from src.phase.Phase import Phase


class Config:
    MUSIC_DIR = "static/music"
    SFX_DIR = "static/sfx"
    CHUNK_SIZE = 1024
    CROSSFADE_TIME = 3000
    PHASES = [
        Phase(
            order=1,
            name="Phase A - Intro",
            directory="phase_A_intro"
        ),
        Phase(
            order=2,
            name="Phase B - Buildup",
            directory="phase_B_buildup"
        ),
        Phase(
            order=3,
            name="Phase C - Peak",
            directory="phase_C_peak"
        ),
        Phase(
            order=4,
            name="Phase D - Descent",
            directory="phase_D_descent"
        ),
        Phase(
            order=5,
            name="Phase E - Welcome back",
            directory="phase_E_welcomeback"
        )
    ]
