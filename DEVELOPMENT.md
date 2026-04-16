# Development Guide

Guide pour développer et étendre Linkora localement.

## Prérequis

- Python 3.6+
- Bash
- Git

## Installation de développement

```bash
git clone https://github.com/Joseph2202HF/linkora.git
cd linkora

# Option 1 : Pas d'installation globale (recommandé pour dev)
./bin/linkora --server

# Option 2 : Installation locale
bash install.sh
# Puis choisir option 2 ou 3
```

## Architecture

### Flux de transfert

```
Client              Serveur
  |                   |
  | ---> Connect      |
  |                   |
  | ---> Envoie data  |
  |                   | (Écrit fichier)
  | ---> Ferme conn   |
  |                   |
  |      Terminé      |
```

### Composants clés

#### main.py
Gère le CLI et route vers client/server:
```python
python main.py --server          # Lance serveur
python main.py --client file.txt # Lance client
```

#### core/server.py
- Bind sur HOST:PORT
- Écoute les connexions entrantes
- Reçoit les données en chunks de BUFFER_SIZE
- Écrit dans un fichier

#### core/client.py
- Connecte à HOST:PORT
- Lit un fichier en chunks
- Envoie les données au serveur
- Ferme la connexion

#### utils/config.py
Paramètres globaux:
```python
HOST = "127.0.0.1"      # Adresse IP
PORT = 2026           # Port TCP
BUFFER_SIZE = 1024      # Taille chunks (bytes)
```

## Flux de développement typique

### 1. Créer une branche
```bash
git checkout -b feature/nouvelle-fonctionnalite
```

### 2. Faire les changements
Exemple : Ajouter affichage de la progression
```python
# core/client.py
file_size = os.path.getsize(filename)
sent = 0
while data:
    client.send(data)
    sent += len(data)
    progress = (sent / file_size) * 100
    print(f"Progression : {progress:.1f}%")
    data = file.read(1024)
```

### 3. Tester localement
Terminal 1 :
```bash
./bin/linkora --server
```

Terminal 2 :
```bash
./bin/linkora --client fichier.txt
```

### 4. Committer
```bash
git add .
git commit -m "Ajout affichage progression du transfert"
```

### 5. Push et PR
```bash
git push origin feature/nouvelle-fonctionnalite
```

Puis créer une Pull Request sur GitHub.

## Améliorations futures

### Courte terme
- [ ] Vérification existence fichier avant envoi
- [ ] Meilleure gestion d'erreurs
- [ ] Logs structurés

### Moyen terme
- [ ] Support multiples connexions (threading)
- [ ] Barre de progression avec `tqdm`
- [ ] Compression fichiers
- [ ] Tests unitaires

### Long terme
- [ ] Chiffrement TLS/SSL
- [ ] Web UI
- [ ] Support REST API
- [ ] Déploiement Docker

## Debugging

### Voir les logs détaillés
```bash
python -u main.py --server
```

### Tester avec des fichiers de test
```bash
# Créer fichier de test
dd if=/dev/urandom of=test_10mb.bin bs=1M count=10

# Envoyer
./bin/linkora --client test_10mb.bin
```

### Vérifier la connexion
```bash
netstat -tlnp | grep 5000
```

## Style de code

Respectez les conventions :
- Variable names : `snake_case`
- Function names : `snake_case()`
- Constants : `UPPER_CASE`
- Classes : `PascalCase`

Exemple :
```python
def send_file_data(client, filename):
    """Envoyer les données d'un fichier via socket."""
    buffer_size = 1024
    with open(filename, "rb") as f:
        data = f.read(buffer_size)
        while data:
            client.send(data)
            data = f.read(buffer_size)
```

## Ressources

- [Python sockets docs](https://docs.python.org/3/library/socket.html)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Linkora Issues](https://github.com/Joseph2202HF/linkora/issues)

## Questions ?

Ouvrez une issue ou contactez les mainteneurs.
