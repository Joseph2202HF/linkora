import socket
from utils.config import SERVER_HOST, PORT


def run_server(host=None):
    host = host or SERVER_HOST
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, PORT))
        server.listen(1)

        print(f"Serveur en attente sur {host}:{PORT}...")

        conn, addr = server.accept()
        print("Connecté :", addr)

        filename = input("Entrez le nom du fichier de destination : ")
        with open(filename, "wb") as file:
            data = conn.recv(1024)
            while data:
                file.write(data)
                data = conn.recv(1024)

        conn.close()
        server.close()
        print("Fichier reçu ✔️")
    except Exception as e:
        print(f"Erreur : {e}")


if __name__ == "__main__":
    run_server()
