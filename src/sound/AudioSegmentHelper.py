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
