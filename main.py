import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="Linkora - Transfert de fichiers")
    parser.add_argument("--server", action="store_true", help="Lancer le serveur")
    parser.add_argument("--client", type=str, help="Lancer le client avec le fichier spécifié")

    args = parser.parse_args()

    if args.server:
        import core.server
    elif args.client:
        import core.client
    else:
        print("Utilisez --server ou --client fichier")
        sys.exit(1)

if __name__ == "__main__":
    main()
