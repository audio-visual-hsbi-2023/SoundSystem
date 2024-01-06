import logging
import socket
from queue import Queue
from threading import Thread

from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server


def handle_osc_message(addr, fixed_args, *args):
    instance: SoundSystemServer = fixed_args[0]
    msg = args[0]
    logging.debug(f"Received OSC message:\n{msg}\n--------")

    raw_data = msg.split("$")[0]
    instance.data_queue.put(raw_data)


class SoundSystemServer(Thread):
    MSG_SIZE = 1024
    DEFAULT_IP = "127.0.0.1"
    DEFAULT_PORT = 8999

    def __init__(self, data_queue: Queue, ip=DEFAULT_IP, port=DEFAULT_PORT):
        super().__init__()
        self.data_queue = data_queue
        self.ip = ip
        self.port = port

        self.dispatcher = Dispatcher()
        self.dispatcher.map("/command", handle_osc_message, self)

        self.server = osc_server.BlockingOSCUDPServer((self.ip, self.port), self.dispatcher)

    def __del__(self):
        logging.debug("Shutting down and closing socket...")
        self.server.shutdown()

    def run(self):
        self.server.serve_forever()
