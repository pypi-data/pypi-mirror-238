
import os
import rabbitpy
from typing import List, Tuple

from inoopa_logging import create_logger
from exceptions import MissingEnvVariable

_logger = create_logger("INOOPA.UTILS.RABBITMQ_HELPERS")


def _get_credentials_from_env() -> Tuple[str, str, str]:
    env_variables = {
        "queue_host": os.getenv("QUEUE_HOST"),
        "queue_username": os.getenv("QUEUE_USERNAME"),
        "queue_password": os.getenv("QUEUE_PASSWORD"),
    }

    missing_variables = []
    for key, value in env_variables.items():
        if value is None:
            _logger.error(f"QUEUE env variable missing: {key}")
            missing_variables.append(key)
    if len(missing_variables) > 0:
        raise MissingEnvVariable(f"Missing env variables: {missing_variables}")

    return env_variables["queue_host"], env_variables['queue_username'], env_variables['queue_password']

def _get_queue_name_with_env(queue_name: str) -> str:
    """Helper function to add the env name to the queue name."""
    env_name = os.getenv("ENV")
    if env_name is None:
        raise MissingEnvVariable("Missing env variable: ENV")
    return f"{queue_name}_{env_name}"

def get_messages_from_queue(queue_name: str, queue_batch_size: int = 1) -> List[str]:
    """Helper function to get X messages from a rabbitMQ queue."""
    host, username, password = _get_credentials_from_env()
    queue_name_with_env = _get_queue_name_with_env(queue_name)
    messages_body = []
    _logger.info(f"Connecting to queue: {queue_name_with_env}...")
    with rabbitpy.Connection(f"amqp://{username}:{password}@{host}/%2f") as conn:
        with conn.channel() as channel:
            queue = rabbitpy.Queue(channel, queue_name_with_env, durable=True)
            queue.declare()
            _logger.info("Connected to queue, reading messages...")
            for i in range(queue_batch_size):
                message = queue.get(acknowledge=True)
                if message:
                    messages_body.append(message.body.decode())
                    # Tell the queue that this message has been read and should be removed from queue
                    message.ack()
                    _logger.info(f"Message {i+1}/{queue_batch_size} read")
                else:
                    _logger.info("Queue empty, stoping...")
                    break
    return messages_body

def push_to_queue(queue_name: str, message: str) -> None:
    """Helper function to push a message to a rabbitMQ queue."""
    host, username, password = _get_credentials_from_env()
    queue_name_with_env = _get_queue_name_with_env(queue_name)

    _logger.info(f"Connecting to queue: {queue_name_with_env}...")
    with rabbitpy.Connection(f"amqp://{username}:{password}@{host}/%2f") as conn:
        with conn.channel() as channel:
            queue = rabbitpy.Queue(channel, queue_name_with_env, durable=True)
            queue.declare()
            
            # Create a new message
            msg = rabbitpy.Message(channel, message)
            
            # Publish the message to the specified queue
            msg.publish('', queue_name_with_env)
            _logger.info(f"Message pushed to {queue_name_with_env}.")
