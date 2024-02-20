import logging
import argparse
import sys

from queue import Queue

from src.command.CommandCenter import Command, CommandType, CommandCenter
from src.sound.sfx.SfxSound import SfxSound
from src.server.SoundSystemServer import SoundSystemServer
from src.sound.music.BackgroundMusic import BackgroundMusic



def normalize_angle_to_float(angle: float) -> float:
    # Normalize the angle to the range [0, 1]
    return angle / 90.0


def play_sfx(command: Command):
    sound = command.str_value
    if sound not in CommandCenter.AVAILABLE_SFX:
        logging.error(f"Unknown SFX {sound}")
        return

    angle = command.num_value
    if angle < -90 or angle > 90:
        logging.error("Unknown angle, falling to closest")
        if angle < -90:
            angle = -90
        else:
            angle = 90

    sfx = SfxSound(sound, normalize_angle_to_float(angle))
    sfx.start()


def main():
    data_queue = Queue()
    server = SoundSystemServer(data_queue)
    bgm = BackgroundMusic()

    logging.debug("Starting background threads for server and music...")
    server.start()
    bgm.start()

    while True:
        logging.debug("waiting for incoming command...")
        data = data_queue.get()
        logging.debug(f"Received data:\n{data}")
        command = Command.str_to_command(data)
        logging.debug(f"Got command {command}")

        match command.command_type:
            case CommandType.START:
                bgm.play_music()
            case CommandType.EXIT:
                sys.exit(0)
            case CommandType.NEXT_SONG:
                bgm.next_song()
            case CommandType.SFX:
                play_sfx(command)
            case CommandType.PHASE_CHANGE:
                bgm.next_phase()
            case _:
                raise ValueError("Unknown command")


# ---------------------------------------
# ---------------------------------------
# ---------------------------------------

if __name__ == "__main__":
    log_level = logging.WARNING
    logging.basicConfig(level=logging.DEBUG)
    main()
