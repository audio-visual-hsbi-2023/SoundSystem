from threading import Thread

from pydub import AudioSegment


class AudioSegmentAsyncLoader(Thread):
    def __init__(self, filename):
        super().__init__()
        self.audio_data: AudioSegment | None = None
        self._filename = filename

    def run(self):
        self.audio_data = AudioSegment.from_wav(self._filename)