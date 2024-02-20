import logging
import os
import pathlib
import random
from queue import Queue
from threading import Thread, Event

import pyaudio
import time
from pydub import AudioSegment

from src.sound.audio.AudioSegmentAsyncLoader import AudioSegmentAsyncLoader
from src.conf.Config import Config
from src.sound.audio import AudioSegmentHelper


class Profiler:
    def __init__(self):
        self.start_stamp = 0
        self.end_stamp = 0

    def start(self):
        self.start_stamp = time.perf_counter()

    def end(self):
        self.end_stamp = time.perf_counter()

    @property
    def time_elapsed(self):
        return self.end_stamp - self.start_stamp


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
        self.ms_ctr = 0
        self.loading = False

        self.profiler = Profiler()
        self.pause_music()

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
        if self.song_ctr >= len(self.current_phase):
            self.song_ctr = 0
            random.shuffle(self.current_phase)

    def update_phase(self):
        # check if already is at last phase
        if self.phase_ctr == len(self.phases) - 1:
            logging.error("Can't continue with p hases. Already the last!")
            return

        self.phase_ctr += 1
        self.current_phase = self.phases[self.phase_ctr]
        self.song_ctr = 0
        self.next_song()

    def run(self):
        self.current_phase = self.phases[self.phase_ctr]
        song = self.current_phase[self.song_ctr]
        self.segment = AudioSegmentHelper.load_audio_segment(str(song))
        self.ms_ctr = AudioSegmentHelper.ms_to_segment_chunk_index(self.segment, 1)
        while True:
            stream = self.audio.open(
                format=self.audio.get_format_from_width(self.segment.sample_width),
                channels=self.segment.channels,
                rate=self.segment.frame_rate,
                output=True
            )

            chunks = AudioSegmentHelper.into_chunks(self.segment)
            chunk_ctr = 0
            self.loading = None
            loader: AudioSegmentAsyncLoader | None = None
            while chunk_ctr <= len(chunks):
                if loader is not None and self.loading and not loader.is_alive():
                    self.loading = False
                    break

                change = False
                if self.next_phase_event.is_set():
                    self.update_phase()
                    self.next_phase_event.clear()
                    change = True
                if self.next_song_event.is_set():
                    self.update_song_ctr()
                    self.next_song_event.clear()
                    change = True
                if change:
                    loader = AudioSegmentAsyncLoader(str(self.current_phase[self.song_ctr]))
                    loader.start()
                    self.loading = True

                if self.pause_event.is_set():
                    continue

                if chunk_ctr >= len(chunks) and loader.is_alive():
                    break

                stream.write(chunks[chunk_ctr])
                chunk_ctr += 1

                if (((len(chunks) - 1) * Config.CHUNK_SIZE) - self.ms_ctr * (Config.CROSSFADE_TIME + 1500)) <= \
                        chunk_ctr * Config.CHUNK_SIZE <= \
                        ((len(chunks) * Config.CHUNK_SIZE) - (self.ms_ctr * (Config.CROSSFADE_TIME + 1500))):
                    self.next_song()

                # END OF WHILE (chunks)
                # ---------------------

            stream.close()
            if self.phase_ctr == len(self.phases):
                break

            if loader is None:
                raise ValueError("No data loaded")

            while loader.is_alive():
                # Wait until audio is loaded
                pass

            self.profiler.start()
            ctr_in_ms = (chunk_ctr * Config.CHUNK_SIZE) / self.ms_ctr
            current_audio_end = self.segment[ctr_in_ms:(ctr_in_ms+Config.CROSSFADE_TIME)]
            self.segment = current_audio_end.append(loader.audio_data, crossfade=Config.CROSSFADE_TIME)
            self.profiler.end()
            logging.debug(f"Time elapsed for preparing new audio segment {self.profiler.time_elapsed}")

        # END OF WHILE
        # ------------

        logging.debug("Phases done. End Music...")
