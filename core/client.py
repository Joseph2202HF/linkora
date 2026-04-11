import socket
from utils.config import HOST, PORT

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

filename = "test.txt"

file = open(filename, "rb")
data = file.read(1024)

while data:
    client.send(data)
    data = file.read(1024)

file.close()
client.close()

print("Fichier envoyé ✔️")
