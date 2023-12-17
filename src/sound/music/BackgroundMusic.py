import logging
import os
import pathlib
import random
from queue import Queue
from threading import Thread, Event

import pyaudio
from pydub import AudioSegment

from src.conf.Config import Config
from src.sound import AudioSegmentHelper


class BackgroundMusic(Thread):
    @staticmethod
    def read_music_filenames():
        music_dirs = list(
            map(lambda x: os.path.abspath(os.path.join(Config.MUSIC_DIR, x.directory)), Config.PHASES)
        )
        phases = []
        for m_dir in music_dirs:
            paths = list(pathlib.Path(m_dir).glob('**/*'))
            abs_paths = list(map(lambda x: x.absolute(), paths))
            random.shuffle(abs_paths)
            phases.append(abs_paths)
        return phases

    def __init__(self):
        super().__init__()
        self.phases = BackgroundMusic.read_music_filenames()
        self.audio = pyaudio.PyAudio()
        self.song_queue = Queue()
        self.play_event = Event()
        self.stop_event = Event()
        self.pause_event = Event()
        self.queue_event = Event()
        self.next_song_event = Event()
        self.next_phase_event = Event()

        self.phase_ctr = 0
        self.song_ctr = 0
        self.current_phase = self.phases[self.phase_ctr]
        random.shuffle(self.current_phase)
        self.segment = None

    def __del__(self):
        self.audio.terminate()

    def play_music(self):
        self.play_event.set()
        self.pause_event.clear()

    def pause_music(self):
        self.pause_event.set()
        self.play_event.clear()

    def stop_music(self):
        self.stop_event.set()

    def queue_song(self, filename):
        print(filename)
        # TODO: implement method to get song by filename
        self.queue_event.set()

    def next_song(self):
        self.next_song_event.set()

    def next_phase(self):
        self.next_phase_event.set()

    def update_song_ctr(self):
        self.song_ctr += 1
        if self.song_ctr == len(self.current_phase):
            self.song_ctr = 0
            random.shuffle(self.current_phase)

    def run(self):
        self.current_phase = self.phases[self.phase_ctr]
        song = self.current_phase[self.song_ctr]
        # TODO remove magic numbers
        self.segment = AudioSegment.from_wav(str(song))[30000:-10000]
        while True:
            stream = self.audio.open(
                format=self.audio.get_format_from_width(self.segment.sample_width),
                channels=self.segment.channels,
                rate=self.segment.frame_rate,
                output=True
            )

            chunks = AudioSegmentHelper.into_chunks(self.segment)
            chunk_ctr = 0

            while chunk_ctr <= len(chunks):
                change = False
                if self.next_phase_event.is_set():
                    self.phase_ctr += 1
                    self.next_phase_event.clear()
                    change = True
                if self.next_song_event.is_set():
                    self.update_song_ctr()
                    self.next_song_event.clear()
                    change = True
                if change:
                    break

                if self.pause_event.is_set():
                    continue

                stream.write(chunks[chunk_ctr])
                chunk_ctr += 1

                if chunk_ctr == len(chunks):
                    self.next_song()

                # END OF WHILE (chunks)

            stream.close()
            if self.phase_ctr == len(self.phases):
                break

            current_audio_end = self.segment._spawn(chunks[chunk_ctr:])[:Config.CROSSFADE_TIME]
            # TODO remove magic numbers
            next_audio = AudioSegment.from_wav(str(self.current_phase[self.song_ctr]))[30000:-10000]
            self.segment = current_audio_end.append(next_audio, crossfade=Config.CROSSFADE_TIME)

        # END OF WHILE

        logging.debug("Phases done. End Music...")
