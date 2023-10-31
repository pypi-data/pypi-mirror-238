import asyncio
import json
import pickle
import time
import traceback
from asyncio import AbstractEventLoop
from functools import wraps
from typing import Any, Awaitable, Callable, Union

import aio_pika
from aio_pika.abc import (AbstractChannel, AbstractConnection,
                          AbstractRobustChannel, AbstractRobustConnection)
from aiormq import AMQPError, ChannelInvalidStateError


class RabbitMQConnection:
    timeout_robust: int = 5
    MAX_RETRIES: int = 10

    def __init__(
            self,
            host: str,
            port: int = 5672,
            user: str = None,
            password: str = None,
            logger: Any = None,
            loop: AbstractEventLoop = asyncio.get_event_loop()
    ) -> None:
        self.__at_started = True
        self._start_time = time.time()
        asyncio.set_event_loop(loop)
        self.url = f'amqp://{user}:{password}@{host}:{port}/'
        self.logger = logger
        self.loop = loop
        self.connection = None
        self.channel = None
        self._robust = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.aio_stop()

    def _check_at_started(self) -> bool:
        if self.__at_started:
            if time.time() - self._start_time > self.timeout_robust:
                self.__at_started = False
        return self.__at_started

    @staticmethod
    def _check_is_open(connection_or_channel) -> bool:
        if connection_or_channel is None or connection_or_channel.is_closed:
            return False
        return True

    async def _close_if_open(self, connection_or_channel):
        if self._check_is_open(connection_or_channel):
            await connection_or_channel.close()

    async def _close_connection(self):
        await self._close_if_open(self.connection)
        self.connection = None

    async def _close_channel(self):
        await self._close_if_open(self.channel)
        self.channel = None

    async def _get_or_create_connection(
            self,
            robust: bool
    ) -> Union[AbstractRobustConnection, AbstractConnection]:
        if self._check_is_open(self.connection):
            return self.connection
        if robust:
            self.connection = await aio_pika.connect_robust(
                self.url, timeout=self.timeout_robust)
        else:
            self.connection = await aio_pika.connect(
                self.url, timeout=self.timeout_robust)

    async def _get_or_create_channel(self, robust: bool = None):
        if self._check_is_open(self.channel):
            return self.channel
        self.logger.info('Channel is closed.')
        await self._get_or_create_connection(robust or self._robust)
        self.channel = await self.connection.channel(on_return_raises=True)
        return self.channel

    async def _get_channel(
            self,
            robust: bool = None
    ) -> Union[AbstractRobustChannel, AbstractChannel]:
        while True:
            if robust is None:
                robust = self._robust
            try:
                return await self._get_or_create_channel(robust)
            except (AMQPError, ConnectionError) as exc:
                trace = traceback.format_exc()
                self.logger.error(f'Error: {exc}. Traceback: {trace}')
                await self.aio_stop()
                await asyncio.sleep(self.timeout_robust)

    async def get_channel(
            self,
            robust: bool,
    ) -> Union[AbstractRobustChannel, AbstractChannel]:
        self._robust = robust
        return await self._get_channel()

    async def get_one_time_use_channel(
            self
    ) -> Union[AbstractRobustChannel, AbstractChannel]:
        return await self._get_channel(robust=False)

    async def aio_stop(self) -> None:
        await self._close_channel()
        await self._close_connection()

    def stop(self) -> None:
        self.loop.run_until_complete(self.aio_stop())

    @staticmethod
    def retry_operation(func) -> Callable:
        @wraps(func)
        async def wrapper(
                self,
                queue_name: str,
                channel: aio_pika.abc.AbstractChannel,
                *args,
                **kwargs
        ):
            for attempt in range(self.MAX_RETRIES):
                try:
                    return await func(self, queue_name, channel,
                                      *args, **kwargs)
                except (
                        AMQPError, ChannelInvalidStateError
                ) as exc:
                    await self.aio_stop()
                    channel = await self._get_channel()
                    self.logger.error(
                        f'Error in function {func.__name__}, {attempt=}:\n'
                        f'Error: {exc}\nTraceback: {traceback.format_exc()}'
                    )
                    if attempt == self.MAX_RETRIES - 1:
                        raise exc
                    await asyncio.sleep(self.timeout_robust)
                    self.logger.info(
                        f'{func.__name__}: Unable to execute. Retrying...'
                    )
                except ConnectionError as exc:
                    self.logger.error(
                        f'Error in function {func.__name__}, {attempt=}:\n'
                        f'Error: {exc}\nTraceback: {traceback.format_exc()}'
                    )
                    if attempt == self.MAX_RETRIES - 1:
                        raise exc
                    await asyncio.sleep(self.timeout_robust)
                    self.logger.info(
                        f'{func.__name__=}: Unable to execute. Retrying...'
                    )
        return wrapper

    async def send_message(
            self,
            queue_name: str,
            channel: aio_pika.abc.AbstractChannel,
            *args: Any,
            json_msg: dict = False,
            expiration: int = None,
    ) -> None:
        if json_msg:
            packed_data = json.dumps(json_msg).encode('utf-8')
        else:
            packed_data = pickle.dumps(args)
        message = aio_pika.Message(body=packed_data, expiration=expiration)
        for attempt in range(self.MAX_RETRIES):
            try:
                await channel.default_exchange.publish(
                    message,
                    routing_key=queue_name
                )
                break
            except (
                    AMQPError, ChannelInvalidStateError
            ) as exc:
                await self.aio_stop()
                channel = await self._get_channel()
                trace = traceback.format_exc()
                self.logger.error(
                    f'{attempt=}: Error: {exc} Traceback: {trace}'
                )
                if attempt == self.MAX_RETRIES - 1:
                    raise exc
                await asyncio.sleep(self.timeout_robust)
                self.logger.info('Unable to execute. Retrying...')
            except ConnectionError as exc:
                trace = traceback.format_exc()
                self.logger.error(
                    f'{attempt=}: Error: {exc} Traceback: {trace}'
                )
                if attempt == self.MAX_RETRIES - 1:
                    raise exc
                await asyncio.sleep(self.timeout_robust)
                self.logger.info('Unable to execute. Retrying...')

    async def callback_handler(
            self,
            queue_name: str,
            channel: aio_pika.abc.AbstractChannel,
            callback: Callable[[Any], Awaitable[None]],
            unpacked_data: list[Any],
    ) -> None:
        try:
            await callback(*unpacked_data)
        except BaseException as exc:
            try:
                traceback_str = ''.join(traceback.format_tb(exc.__traceback__))
            except Exception:
                traceback_str = 'Traceback is not available.'
            exception_message = (f'Error: {type(exc)}: {str(exc)}\n'
                                 f'{traceback_str}')
            await self.send_message(
                queue_name, channel, exc, exception_message, expiration=5
            )

    async def consume_queue(
            self,
            queue_name: str,
            channel: aio_pika.abc.AbstractChannel,
            callback: Callable[[Any], Awaitable[None]],
            create_task: bool = True,
            json_msg: bool = False,
    ) -> None:
        if not self._check_is_open(channel):
            channel = await self._get_channel()
        queue = await channel.declare_queue(queue_name, durable=True)
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    try:
                        if json_msg:
                            unpacked_data = [json.loads(message.body)]
                        else:
                            unpacked_data = pickle.loads(message.body)
                    except BaseException as exc:
                        self.logger.error(
                            f'Error: {exc}\n'
                            f'Traceback: {traceback.format_exc()}'
                        )
                        continue
                    if create_task:
                        if len(unpacked_data) and isinstance(
                                unpacked_data[0], BaseException):
                            raise RuntimeError(unpacked_data[1])
                        else:
                            asyncio.create_task(
                                self.callback_handler(
                                    queue_name, channel, callback,
                                    unpacked_data
                                )
                            )
                    else:
                        await callback(*unpacked_data)
