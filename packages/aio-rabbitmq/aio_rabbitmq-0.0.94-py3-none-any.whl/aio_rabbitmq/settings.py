from dataclasses import dataclass


@dataclass
class RabbitMQSettings:
    """
    Class for RabbitMQ settings.
    """
    host: str = 'localhost'
    port: int = 5672
    username: str = 'rabbitmq'
    password: str = 'rabbitmq'
    prefix: str = ''
