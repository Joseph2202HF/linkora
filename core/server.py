import socket
from utils.config import HOST, PORT

try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)

    print("Serveur en attente...")

    conn, addr = server.accept()
    print("Connecté :", addr)

    filename = input("Entrez le nom du fichier de destination : ")
    file = open(filename, "wb")

    data = conn.recv(1024)
    while data:
        file.write(data)
        data = conn.recv(1024)

    file.close()
    conn.close()
    server.close()

    print("Fichier reçu ✔️")
except Exception as e:
    print(f"Erreur : {e}")
