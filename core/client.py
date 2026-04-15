import socket
from utils.config import CLIENT_HOST, PORT


def run_client(filename=None, host=None):
    host = host or CLIENT_HOST
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, PORT))

        if not filename:
            filename = input("Entrez le nom du fichier à envoyer : ")

        with open(filename, "rb") as file:
            data = file.read(1024)
            while data:
                client.send(data)
                data = file.read(1024)

        client.close()
        print("Fichier envoyé ✔️")
    except Exception as e:
        print(f"Erreur : {e}")


if __name__ == "__main__":
    run_client()
