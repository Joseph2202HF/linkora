# Linkora

Un projet open source simple pour le transfert de fichiers en Python via sockets TCP.

## Fonctionnalités
- Transfert de fichiers entre client et serveur.
- Support des fichiers binaires.
- Interface simple en ligne de commande.

## Installation
1. Clonez le dépôt :
   ```bash
   git clone https://github.com/votre-utilisateur/linkora.git
   cd linkora
   ```
2. Assurez-vous d'avoir Python 3.x installé.

## Usage
1. Lancez le serveur :
   ```bash
   python main.py
   # Choisissez 1 pour serveur
   ```
2. Dans un autre terminal, lancez le client :
   ```bash
   python main.py
   # Choisissez 2 pour client, puis entrez le nom du fichier
   ```

## Configuration
Modifiez `utils/config.py` pour changer l'hôte, le port ou la taille du buffer.

## Contribution
Les contributions sont les bienvenues ! Ouvrez une issue ou une pull request.

## Licence
Ce projet est sous licence MIT.
