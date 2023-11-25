class CommandCenter:
    PLAY_MUSIC_REGEX = r"^(PLAY_MUSIC|NEXT_SONG|PAUSE_SONG);_;0$"
    PLAY_SFX_REGEX = r"^PLAY_SFX;.{1,50};(-?[0-9]|[1-8][0-9]|90)$"
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
