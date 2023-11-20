from threading import Thread
from openal.audio import *
from openal.loaders import load_wav_file
from openal import al, alc
from conf.Config import Config
from openal import *
from pydub import AudioSegment

import os
import pathlib
import wave
import pyaudio
import time
import random
import math


class BackgroundMusic(Thread):
    @staticmethod
    def _audio_segment_into_chunks(segment: AudioSegment):
        cs = Config.CHUNK_SIZE
        data = segment.raw_data
        i = 0
        chunks = []
        while i < len(data):
            chunks.append(data[i:i + cs])
            i += cs
        return chunks

    @staticmethod
    def read_music_filenames():
        music_dirs = list(
            map(lambda x: os.path.abspath(os.path.join(Config.MUSIC_DIR, x.directory)), Config.PHASES))
        phases = []
        for m_dir in music_dirs:
            paths = list(pathlib.Path(m_dir).glob('**/*'))
            abs_paths = list(map(lambda x: x.absolute(), paths))
            # random.shuffle(abs_paths)
            phases.append(abs_paths)
        return phases

    def __init__(self):
        super().__init__()
        self.phases = BackgroundMusic.read_music_filenames()
        self.audio = pyaudio.PyAudio()

    def __del__(self):
        self.audio.terminate()

    def run(self):
        # data, samplerate = soundfile.read(song_a)
        # soundfile.write(song_a, data, samplerate)

        for phase in self.phases:
            for song in phase:
                with wave.open(str(song), 'rb') as wf:
                    stream = self.audio.open(
                        format=self.audio.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True
                    )

                    song = AudioSegment.from_wav(str(song))
                    r_song = song.reverse()
                    assert(song.raw_data != r_song.raw_data)
                    chunks = BackgroundMusic._audio_segment_into_chunks(r_song)
                    for chunk in chunks:
                        stream.write(chunk)
                    # while len(data := wf.readframes(Config.CHUNK_SIZE)):
                    #    stream.write(data)

                    stream.close()


class SfxSound(Thread):
    @staticmethod
    def get_absolute_sfx_filepath(f):
        return os.path.abspath(os.path.join(Config.SFX_DIR, f))

    def __init__(self, filename):
        super().__init__()
        self.filename = SfxSound.get_absolute_sfx_filepath(filename)
        self.sink = SoundSink()
        self.sink.listener = SoundListener()

    def run(self):
        """
        source = oalOpen(str(self.filename))
        source.play()
        while source.get_state() == AL_PLAYING:
            time.sleep(1)
        oalQuit()
        source = SoundSource()
        wav = load_wav_file(str(self.filename))
        source.queue(wav)
        self.sink.play(source)
        """


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
