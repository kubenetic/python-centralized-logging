import logging

from reconnecting_socket_handler import ReconnectingSocketHandler


def setup_tcp_logger(host: str = '127.0.0.1', port: int = 3200) -> logging.Logger:
    """
    Set up a logger that sends logs to a TCP server.

    Args:
        host (str): Host of the server.
        port (int): Port of the server.

    Returns:
        logging.Logger: Logger instance.
    """
    logger = logging.getLogger('client')
    logger.setLevel(logging.INFO)

    socket_handler = ReconnectingSocketHandler(host, port)
    logger.addHandler(socket_handler)

    return logger


if __name__ == '__main__':
    # Get a logger instance
    logger = setup_tcp_logger()

    # Log some messages
    logger.info("This is a test message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
