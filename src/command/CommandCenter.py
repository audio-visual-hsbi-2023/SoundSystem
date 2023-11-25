from __future__ import annotations

import enum
import re


class CommandType(enum.Enum):
    MUSIC = 1
    SFX = 2
    PHASE_CHANGE = 3
    START = 4
    EXIT = 5


class Command:
    def __init__(self, command_type: CommandType, command: str, str_value: str, num_value: int):
        self.command_type = command_type
        self.command = command
        self.str_value = str_value
        self.num_value = num_value

    def __str__(self):
        return f"{self.command_type}, {self.command}, {self.str_value}, {self.num_value};"

    @staticmethod
    def str_to_command(string) -> Command:
        if not re.match(CommandCenter.BASIC_REGEX, string):
            raise ValueError(f"Not a proper message!")

        tokens = string.split(";")
        command = tokens[0]
        str_value = tokens[1]
        num_value = int(tokens[2])

        if re.match(CommandCenter.MUSIC_REGEX, string):
            command_type = CommandType.MUSIC
        elif re.match(CommandCenter.SFX_REGEX, string):
            command_type = CommandType.SFX
        elif re.match(CommandCenter.START_REGEX, string):
            command_type = CommandType.START
        elif re.match(CommandCenter.PHASE_CHANGE_REGEX, string):
            command_type = CommandType.PHASE_CHANGE
        elif re.match(CommandCenter.EXIT_REGEX, string):
            command_type = CommandType.EXIT
        else:
            raise ValueError("Unknown command type!")

        return Command(
            command_type=command_type,
            command=command,
            str_value=str_value,
            num_value=num_value
        )


class CommandCenter:
    BASIC_REGEX = r".*;.*;[0-9]+$"
    MUSIC_REGEX = r"^(PLAY_MUSIC|NEXT_SONG|PAUSE_SONG);_;0$"
    SFX_REGEX = r"^PLAY_SFX;.{1,50};(-?[0-9]|[1-8][0-9]|90)$"
    PHASE_CHANGE_REGEX = r"^PHASE_CHANGE;_;([1-5])$"
    EXIT_REGEX = r"^EXIT;_;0$"
    START_REGEX = r"^START;_;0$"

    AVAILABLE_SFX = list(
        map(
            lambda x: f"{x}.wav",
            [
                "birds"
            ]
        )
    )
