import socket
from utils.config import HOST, PORT

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Serveur en attente...")

conn, addr = server.accept()
print("Connecté :", addr)

file = open("received_file", "wb")

data = conn.recv(1024)
while data:
    file.write(data)
    data = conn.recv(1024)

file.close()
conn.close()

print("Fichier reçu ✔️")
