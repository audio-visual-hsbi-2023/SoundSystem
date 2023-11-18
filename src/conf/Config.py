from phase.Phase import Phase


class Config:
    MUSIC_DIR = "static/music"
    SFX_DIR = "static/sfx"
    CHUNK_SIZE = 1024
    PHASES = [
        Phase(
            order=1,
            name="Phase A - Intro",
            directory="phase_A_intro"
        )
    ]
