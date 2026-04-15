import argparse
import sys
from core import server as server_module
from core import client as client_module


def main():
    parser = argparse.ArgumentParser(description="Linkora - Transfert de fichiers", add_help=False)
    parser.add_argument("--help", action="help", help="Afficher cette aide")
    parser.add_argument("--server", action="store_true", help="Lancer le serveur")
    parser.add_argument("--client", type=str, help="Lancer le client avec le fichier spécifié")
    parser.add_argument("-H", "--host", type=str, help="Adresse IP du serveur à utiliser pour le client")

    args = parser.parse_args()

    if args.server:
        server_module.run_server()
    elif args.client:
        client_module.run_client(filename=args.client, host=args.host)
    else:
        print("Utilisez --server ou --client fichier")
        sys.exit(1)


if __name__ == "__main__":
    main()
