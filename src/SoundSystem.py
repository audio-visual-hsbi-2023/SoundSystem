from threading import Thread
from conf.Config import Config
from openal import *

import os
import pathlib
import wave
import pyaudio
import time


class BackgroundMusic(Thread):
    @staticmethod
    def read_music_filenames():
        music_dirs = list(
            map(lambda x: os.path.abspath(os.path.join(Config.MUSIC_DIR, x)), os.listdir(Config.MUSIC_DIR)))
        phases = []
        for m_dir in music_dirs:
            paths = list(pathlib.Path(m_dir).glob('**/*'))
            abs_paths = list(map(lambda x: x.absolute(), paths))
            phases.append(abs_paths)
        return phases

    def __init__(self):
        super().__init__()
        self.phases = BackgroundMusic.read_music_filenames()

    def run(self):
        song_a = str(self.phases[0][0])

        # data, samplerate = soundfile.read(song_a)
        # soundfile.write(song_a, data, samplerate)

        with wave.open(song_a, 'rb') as wf:
            p = pyaudio.PyAudio()
            stream = p.open(
                format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True
            )

            while len(data := wf.readframes(Config.CHUNK_SIZE)):
                stream.write(data)

            stream.close()
            p.terminate()

class SfxSound(Thread):
    @staticmethod
    def get_absolute_sfx_filepath(f):
        return os.path.abspath(os.path.join(Config.SFX_DIR, f))

    def __init__(self, f, x=0, y=0, distance=0):
        super().__init__()
        self.filename = SfxSound.get_absolute_sfx_filepath(f)
        self.x = x
        self.y = y
        self.distance = distance

    def run(self):
        source = oalOpen(str(self.filename))
        source.play()
        while source.get_state() == AL_PLAYING:
            time.sleep(1)
        oalQuit()


if __name__ == "__main__":
    bgm = BackgroundMusic()
    sfx = SfxSound("birds.wav")

    print("Start playing background music...")
    bgm.start()

    print("wait a moment...")
    for i in range(0, 3):
        print(i)
        time.sleep(1)

    print("Play bird tweeting...")
    sfx.start()
