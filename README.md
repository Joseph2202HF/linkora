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
2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
3. Installez le package :
   ```bash
   pip install .
   ```
   Puis utilisez `linkora --server` ou `linkora --client fichier`.

Assurez-vous d'avoir Python 3.6+ installé.

## Usage
Lancez le serveur :
```bash
python main.py --server
```

Lancez le client :
```bash
python main.py --client nom_du_fichier
```

Ou utilisez l'ancien mode interactif (obsolète) :
```bash
python main.py
# Puis choisissez 1 ou 2
```

## Configuration
Modifiez `utils/config.py` pour changer l'hôte, le port ou la taille du buffer.

## Contribution
Les contributions sont les bienvenues ! Ouvrez une issue ou une pull request.

## Licence
Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.
