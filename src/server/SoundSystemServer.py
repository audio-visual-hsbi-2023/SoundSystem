import logging
import socket
from queue import Queue
from threading import Thread


class SoundSystemServer(Thread):
    MSG_SIZE = 1024
    DEFAULT_IP = "127.0.0.1"
    DEFAULT_PORT = 8999

    def __init__(self, data_queue: Queue, ip=DEFAULT_IP, port=DEFAULT_PORT):
        super().__init__()
        self.data_queue = data_queue
        self.ip = ip
        self.port = port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip, self.port))
        self.socket.listen()

    def __del__(self):
        logging.debug("Shutting down and closing socket...")
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

    def run(self):
        while True:
            conn, addr = self.socket.accept()
            logging.info(f"Incoming connection from {addr}")
            data = ""
            with conn:
                while True:
                    recvd = conn.recv(SoundSystemServer.MSG_SIZE)
                    if not recvd:
                        break

                    raw_data = str(recvd)[2:-1].split("$")[0]
                    data += raw_data
                    if len(raw_data) < SoundSystemServer.MSG_SIZE:
                        break

            self.data_queue.put(data)
