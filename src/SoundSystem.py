import time

from src.sound.music.BackgroundMusic import BackgroundMusic
from src.sound.sfx.SfxSound import SfxSound

if __name__ == "__main__":
    bgm = BackgroundMusic()

    print("Start playing background music...")
    bgm.start()
    bgm.play_music()

    print("wait a moment...")
    for i in range(1, 3):
        print(i)
        time.sleep(1)

    print("Play bird tweeting on the left...")
    sfx = SfxSound(filename="birds.wav", panning=-1.0)
    sfx.start()
