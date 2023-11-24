import os
from threading import Thread

import pyaudio
from pydub import AudioSegment

from src.conf.Config import Config
from src.sound import AudioSegmentHelper


class SfxSound(Thread):
    @staticmethod
    def get_absolute_sfx_filepath(f):
        return os.path.abspath(os.path.join(Config.SFX_DIR, f))

    def __init__(self, filename, panning=0.0):
        super().__init__()
        self.filename = SfxSound.get_absolute_sfx_filepath(filename)
        self.audio = pyaudio.PyAudio()
        self.panning = panning

    def __del__(self):
        self.audio.terminate()

    def run(self):
        audio = AudioSegment.from_wav(self.filename).pan(self.panning)
        stream = self.audio.open(
            format=self.audio.get_format_from_width(audio.sample_width),
            channels=audio.channels,
            rate=audio.frame_rate,
            output=True
        )

        chunks = AudioSegmentHelper.into_chunks(audio)
        for chunk in chunks:
            stream.write(chunk)

        stream.close()
