import argparse
import sys

parser = argparse.ArgumentParser(description="Linkora - Transfert de fichiers")
parser.add_argument("--server", action="store_true", help="Lancer le serveur")
parser.add_argument("--client", type=str, help="Lancer le client avec le fichier spécifié")

args = parser.parse_args()

if args.server:
    import core.server
elif args.client:
    # Passer le filename au client
    import core.client
    # Mais client utilise input, donc modifier client pour accepter arg
else:
    print("Utilisez --server ou --client fichier")
    sys.exit(1)
