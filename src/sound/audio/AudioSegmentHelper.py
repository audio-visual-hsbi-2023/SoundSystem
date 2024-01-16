from pyaudio import Stream

from src.sound.audio.AudioSegmentAsyncLoader import AudioSegmentAsyncLoader, AsyncLoaderResponse
from src.conf.Config import Config
from pydub import AudioSegment


def into_chunks(segment: AudioSegment, chunk_size=Config.CHUNK_SIZE) -> list[bytes]:
    data = segment.raw_data
    i = 0
    chunks = []
    while i < len(data):
        chunks.append(data[i:i + chunk_size])
        i += chunk_size
    return chunks


def load_audio_segment_and_stream(filename, pyaudio) -> AsyncLoaderResponse:
    loader = AudioSegmentAsyncLoader(filename, pyaudio)
    # loader.start()
    # while loader.is_alive():
    #    pass
    loader.run()
    response = loader.response

    if response is None:
        raise ValueError("Loader returned None data")

    return response


def ms_to_segment_chunk_index(segment: AudioSegment, ms):
    return int(segment.frame_count(ms) * segment.frame_width)
