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

    def run(self):
        phase_ctr = 0
        song_ctr = 0
        while True:
            phase = self.phases[phase_ctr]
            song = phase[song_ctr]
            was_queued = False

            if not self.song_queue.empty():
                song = self.song_queue.get()
                was_queued = True

            audio = AudioSegment.from_wav(str(song))[-3000:]

            stream = self.audio.open(
                format=self.audio.get_format_from_width(audio.sample_width),
                channels=audio.channels,
                rate=audio.frame_rate,
                output=True
            )

            chunks = AudioSegmentHelper.into_chunks(audio)
            chunk_ctr = 0

            # TODO implement transitions between songs
            while chunk_ctr <= len(chunks):
                if self.pause_event.is_set():
                    continue
                elif self.next_song_event.is_set():
                    if not was_queued:
                        song_ctr += 1
                    if song_ctr == len(phase):
                        random.shuffle(phase)
                        song_ctr = 0
                    self.next_song_event.clear()
                    break
                elif self.next_phase_event.is_set():
                    phase_ctr += 1
                    self.next_phase_event.clear()
                    break

                stream.write(chunks[chunk_ctr])
                chunk_ctr += 1

                if chunk_ctr == len(chunks):
                    self.next_song()

            stream.close()
            if phase_ctr == len(self.phases):
                break

        logging.debug("Phases done. End Music...")
