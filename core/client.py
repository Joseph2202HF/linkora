import socket
import struct
import os
from utils.config import CLIENT_HOST, PORT


def run_client(filename=None, host=None):
    host = host or CLIENT_HOST
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, PORT))

        if not filename:
            filename = input("Entrez le nom du fichier à envoyer : ")

        size = os.path.getsize(filename)
        client.send(struct.pack('!Q', size))

        with open(filename, "rb") as file:
            sent = 0
            data = file.read(2048)
            while data:
                client.send(data)
                sent += len(data)
                print(f"Progress: {sent / size * 100:.2f}%")
                data = file.read(2048)

        client.close()
        print("Fichier envoyé ✔️")
    except Exception as e:
        print(f"Erreur : {e}")


if __name__ == "__main__":
    run_client()
