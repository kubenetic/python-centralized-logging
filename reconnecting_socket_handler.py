import logging
import socket
import time
from logging.handlers import SocketHandler
from typing import override


class ReconnectingSocketHandler(SocketHandler):
    """
    A subclass of SocketHandler that reconnects to the server if the connection is lost.
    """

    @override
    def emit(self, record: logging.LogRecord) -> None:
        """
        Emit a record.

        If some type of connection or network error occurs while sending the record, tries to reconnect to the server
        and resend the record.
        """
        try:
            super().emit(record)
        except (socket.error, ConnectionResetError):
            self.retry_connection()
            super().emit(record)
        except Exception:
            self.handleError(record)

    def retry_connection(self, retry_count: int = 5, retry_interval_sec: int = 5) -> None:
        """
        Retry to connect to the server.

        Args:
            retry_count (int): Number of times to retry to connect to the server.
            retry_interval_sec (int): Interval in seconds between each retry.

        Raises:
            ConnectionError: If the connection could not be reestablished after all the retries.
        """
        for _ in range(retry_count):
            try:
                self.createSocket()
                return
            except (socket.error, ConnectionResetError):
                time.sleep(retry_interval_sec)

        raise ConnectionError("Could not reconnect to the server")
