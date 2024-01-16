from threading import Thread

from pyaudio import Stream
from pydub import AudioSegment

from conf.Config import Config
from sound.audio import AudioSegmentHelper


class AsyncLoaderResponse:
    def __init__(self, segment, stream, chunks):
        self.segment = segment
        self.stream = stream
        self.chunks = chunks


class AudioSegmentAsyncLoader(Thread):
    def __init__(self, filename, pyaudio, current_remain=None):
        super().__init__()
        self.response: AsyncLoaderResponse | None = None
        self._filename = filename
        self._current_remain = current_remain
        self._pyaudio = pyaudio

    def run(self):
        new_segment = AudioSegment.from_wav(self._filename)
        if self._current_remain is not None:
            remain = self._current_remain[0][self._current_remain[1]:]
            current_fade_out = remain[:Config.FADE_TIME + 1000]
            new_segment = current_fade_out.append(new_segment, crossfade=Config.FADE_TIME)
        else:
            new_segment = new_segment.fade_in(Config.FADE_TIME).fade_out(Config.FADE_TIME)

        stream = self._pyaudio.open(
            format=self._pyaudio.get_format_from_width(new_segment.sample_width),
            channels=new_segment.channels,
            rate=new_segment.frame_rate,
            output=True
        )

        chunks = AudioSegmentHelper.into_chunks(new_segment)

        self.response = AsyncLoaderResponse(new_segment, stream, chunks)
