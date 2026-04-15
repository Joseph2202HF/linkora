import socket
import struct
from utils.config import SERVER_HOST, PORT


def get_local_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("8.8.8.8", 80))
        return sock.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        sock.close()


def run_server(host=None):
    host = host or SERVER_HOST
    local_ip = get_local_ip() if host == "0.0.0.0" else host
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, PORT))
        server.listen(1)

        print(f"Serveur en attente sur {local_ip}:{PORT}...")

        conn, addr = server.accept()
        print("Connecté :", addr)

        size_data = conn.recv(8)
        size = struct.unpack('!Q', size_data)[0]
        print(f"Taille du fichier attendue : {size} octets")

        filename = input("Entrez le nom du fichier de destination : ")
        with open(filename, "wb") as file:
            received = 0
            while received < size:
                data = conn.recv(2048)
                if not data:
                    break
                file.write(data)
                received += len(data)
                print(f"Progress: {received / size * 100:.2f}%")

        conn.close()
        server.close()
        print("Fichier reçu ✔️")
    except Exception as e:
        print(f"Erreur : {e}")


if __name__ == "__main__":
    run_server()
