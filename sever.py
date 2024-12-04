import logging
import pickle
import socket
import struct
import threading


def start_log_server(host: str = '127.0.0.1', port: int = 3200) -> None:
    """
    Start a log server that listens for incoming log records.

    Args:
        host (str): Host of the server.
        port (int): Port of the server.
    """

    # AF_INET (Address Family) - It indicates the socket will use IPv4 addressing.
    # SOCK_STREAM (Socket Type) - It indicates the socket will use TCP for data transmission.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # SOL_SOCKET - This flag specifies that the option being set or queried applies to the socket layer
    # (i.e., general socket options).
    # SO_KEEPALIVE - This option enables o detect and maintain idle connections and sending keep-alive packets on it.
    # It ensures that the connection remains active even during periods of inactivity by periodically sending small
    # packets (keep-alive probes) to check if the other end is still reachable.
    #
    # Once SO_KEEPALIVE is enabled, the behavior is governed by the operating system’s TCP settings. The following
    # parameters determine how and when keep-alive probes are sent:
    #
    #     Keep-Alive Time:
    #         The time of inactivity before the first keep-alive probe is sent.
    #     Keep-Alive Interval:
    #         The interval between subsequent probes if no response is received.
    #     Keep-Alive Retries:
    #         The number of unanswered probes before the connection is considered broken.
    #
    # Customizing TCP Keep-Alive on Linux
    # sudo sysctl -w net.ipv4.tcp_keepalive_time=60
    # sudo sysctl -w net.ipv4.tcp_keepalive_intvl=10
    # sudo sysctl -w net.ipv4.tcp_keepalive_probes=5
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    server_socket.bind((host, port))
    server_socket.listen(10)

    while True:
        try:
            connection, addr = server_socket.accept()
        except KeyboardInterrupt:
            print("Server stopped")
            break
        except Exception as e:
            print(f"Error: {e}")
            continue

        print(f"Connection established {addr}")
        threading.Thread(target=handle_client, args=(addr, connection)).start()


def handle_client(addr, connection) -> None:
    """
    Handle a client connection.

    Args:
        addr: Address of the client.
        connection: Connection object.
    """
    try:
        while True:
            length_of_data = connection.recv(4)
            if not length_of_data:
                break

            length = struct.unpack('>L', length_of_data)[0]
            log_data = connection.recv(length)
            if not log_data:
                break

            log_record = pickle.loads(log_data)
            print(f"Received log record: {log_record}")

            log_record = logging.makeLogRecord(log_record)
            logger = logging.getLogger(log_record.name)
            logger.handle(log_record)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        connection.close()
        print(f"Connection closed with {addr}")


# Print all logs above DEBUG level and set the format
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
if __name__ == '__main__':
    # Start the log server
    start_log_server()
