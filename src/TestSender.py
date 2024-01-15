from pythonosc import udp_client
from src.server.SoundSystemServer import SoundSystemServer

HOST = SoundSystemServer.DEFAULT_IP
PORT = SoundSystemServer.DEFAULT_PORT

if __name__ == "__main__":
    msgs = [
        "START;_;0$",
        "EXIT;_;0$",
        "NEXT_SONG;_;0$",
        "PHASE_CHANGE;_;0$",
        "PLAY_SFX;cymbal_impact;90$",
    ]
    print("Please select one of the following commands:")
    i = 0
    while i < len(msgs):
        print(f"[{i}]: {msgs[i]}")
        i += 1
    number = int(input(">>> "))

    client = udp_client.SimpleUDPClient(HOST, PORT)
    msg = msgs[number]

    print(f'Sending message "{msg}"')
    client.send_message("/command", msg)
