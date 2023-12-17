import socket

# from src.server.SoundSystemServer import SoundSystemServer


HOST = "127.0.0.1" # SoundSystemServer.DEFAULT_IP
PORT = 8999 # SoundSystemServer.DEFAULT_PORT

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b"NEXT_SONG;_;0$")
        # s.sendall(b"PLAY_SFX;birds;0$")
        data = s.recv(1024)

    print(f"Received {data!r}")
