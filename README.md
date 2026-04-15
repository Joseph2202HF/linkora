# Linkora

Un projet open source simple pour le transfert de fichiers en Python via sockets TCP.

## 🎯 Objectifs

- Transfert fiable de fichiers via sockets TCP
- Interface CLI simple et intuitive
- Code léger et facile à comprendre/modifier
- Plateforme pour apprendre les sockets en Python

## ✨ Fonctionnalités

- Transfert de fichiers entre client et serveur
- Support des fichiers binaires (images, vidéos, etc.)
- Interface simple en ligne de commande avec arguments
- Installation facile avec script Bash
- Commande `linkora` disponible globalement après installation

## 📋 Prérequis

- Python 3.6+
- Bash
- Pas de dépendances externes

## 🚀 Installation

### Via script d'installation (recommandé)

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/Joseph2202HF/linkora.git
   cd linkora
   ```

2. Lancez le script d'installation :
   ```bash
   bash install.sh
   ```

3. Suivez les options :
   - **Option 1** : Copier `linkora` dans `/usr/local/bin` (nécessite sudo)
   - **Option 2** : Ajouter `bin/` à votre PATH
   - **Option 3** : Ne rien faire (utiliser `./bin/linkora` directement)

Une fois installé, utilisez `linkora --server` ou `linkora --client fichier`.

### Utilisation sans installation

```bash
./bin/linkora --server
./bin/linkora --client fichier.txt
```

## 💻 Utilisation

### Lancer le serveur

```bash
linkora --server
# Affiche : Serveur en attente...
```

Le serveur écoute sur `127.0.0.1:5000` (configurable dans `utils/config.py`).

### Envoyer un fichier (client)

Dans un autre terminal :
```bash
linkora --client mon_fichier.txt
# Affiche : Fichier envoyé ✔️
```

### Exemples complets

**Terminal 1 (serveur)**
```bash
$ linkora --server
Serveur en attente...
Connecté : ('127.0.0.1', 54321)
Entrez le nom du fichier de destination : reçu.txt
Fichier reçu ✔️
```

**Terminal 2 (client)**
```bash
$ linkora --client document.pdf
Fichier envoyé ✔️
```

## ⚙️ Configuration

Modifiez `utils/config.py` pour changer les paramètres :

```python
HOST = "127.0.0.1"      # Adresse IP (localhost par défaut)
PORT = 5000             # Port TCP
BUFFER_SIZE = 1024      # Taille des chunks (en bytes)
```

Pour permettre les connexions distantes :
```python
HOST = "0.0.0.0"  # Accepte toutes les interfaces
```

Puis regénérez le serveur et client.

## 📂 Structure du projet

```
linkora/
├── main.py              # Point d'entrée CLI
├── install.sh           # Script d'installation Bash
├── bin/
│   └── linkora          # Wrapper exécutable Bash
├── core/
│   ├── client.py        # Logique client (envoie fichiers)
│   └── server.py        # Logique serveur (reçoit fichiers)
├── utils/
│   └── config.py        # Configuration réseau
├── README.md            # Ce fichier
├── CONTRIBUTING.md      # Guide de contribution
├── DEVELOPMENT.md       # Guide de développement
├── LICENSE              # Licence MIT
└── .gitignore           # Fichiers Git ignorés
```

## 🤝 Contribution

Les contributions sont les bienvenues ! Veuillez lire [CONTRIBUTING.md](CONTRIBUTING.md) pour :
- Comment signaler des bugs
- Comment proposer des améliorations
- Processus de soumission de code
- Guidelines de style

### Idées de contributions
- ✅ Support de plusieurs connexions simultanées
- ✅ Affichage de la barre de progression
- ✅ Chiffrement des données
- ✅ Compression des fichiers
- ✅ Logging structuré
- ✅ Tests unitaires

Consultez [DEVELOPMENT.md](DEVELOPMENT.md) pour débuter.

## 📖 Documentation supplémentaire

- [CONTRIBUTING.md](CONTRIBUTING.md) - Guide complet pour contribuer
- [DEVELOPMENT.md](DEVELOPMENT.md) - Guide de développement pour les contributeurs
- [LICENSE](LICENSE) - Licence MIT

## 🐛 Bugs et Issues

Avez-vous trouvé un bug ? Ouvrez une [issue GitHub](https://github.com/Joseph2202HF/linkora/issues) avec :
- Description du problème
- Étapes pour reproduire
- Version de Python utilisée
- Messages d'erreur complets

## 📝 Licence

Ce projet est sous licence MIT. Voir [LICENSE](LICENSE) pour plus de détails.

## 👨‍💻 Auteurs

- [Joseph2202HF](https://github.com/Joseph2202HF)

## 🙏 Remerciements

Merci à tous les contributeurs et utilisateurs de Linkora !

---

**Commencez maintenant** : `bash install.sh` 🚀
