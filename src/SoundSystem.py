import logging

from queue import Queue

from command.CommandCenter import Command
from src.server.SoundSystemServer import SoundSystemServer
from src.sound.music.BackgroundMusic import BackgroundMusic


def main():
    data_queue = Queue()
    server = SoundSystemServer(data_queue)
    bgm = BackgroundMusic()

    logging.debug("Starting background threads for server and music...")
    server.start()
    bgm.start()
    bgm.play_music()

    while True:
        logging.debug("waiting for incoming command...")
        data = data_queue.get()
        logging.debug(f"Received data:\n{data}")
        command = Command.str_to_command(data)
        logging.debug(f"Got command {command}")

# ---------------------------------------
# ---------------------------------------
# ---------------------------------------

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
