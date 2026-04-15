# Contributing to Linkora

Merci d'être intéressé par la contribution à Linkora ! Ce guide vous expliquera comment participer au projet.

## Table des matières
- [Code of Conduct](#code-of-conduct)
- [Comment contribuer](#comment-contribuer)
- [Processus de développement](#processus-de-développement)
- [Structure du projet](#structure-du-projet)
- [Guidelines](#guidelines)
- [Pull Requests](#pull-requests)

## Code of Conduct

Soyez respectueux, inclusif et constructif dans tous les échanges. Nous valorisons la diversité et créons un environnement accueillant.

## Comment contribuer

### Signaler un bug
1. Vérifiez que le bug n'a pas déjà été rapporté dans les [Issues](https://github.com/Joseph2202HF/linkora/issues)
2. Créez une issue avec :
   - Titre clair et descriptif
   - Description précise du bug
   - Étapes pour reproduire
   - Résultat attendu vs résultat obtenu
   - Version de Python utilisée

### Proposer une amélioration
1. Ouvrez une issue avec le label `enhancement`
2. Décrivez clairement la fonctionnalité souhaitée
3. Expliquez le cas d'usage et les bénéfices

### Soumettre du code

1. **Forker le dépôt**
   ```bash
   git clone https://github.com/votre-compte/linkora.git
   cd linkora
   ```

2. **Créer une branche**
   ```bash
   git checkout -b feature/nom-de-la-feature
   # ou
   git checkout -b bugfix/description-du-bug
   ```

3. **Installer l'environnement de développement**
   ```bash
   bash install.sh
   # Ou directement avec le bin
   ./bin/linkora --server
   ```

4. **Faire vos changements**
   - Modifiez le code
   - Testez localement
   - Assurez-vous que le code suit les conventions

5. **Committer vos changements**
   ```bash
   git add .
   git commit -m "Descriptif clair du changement"
   ```

6. **Pousser vers votre fork**
   ```bash
   git push origin feature/nom-de-la-feature
   ```

7. **Ouvrir une Pull Request**
   - Vers `main` du dépôt officiel
   - Titre clair et concis
   - Description détaillée des changements
   - Référencez les issues liées

## Processus de développement

### Setup local
```bash
git clone https://github.com/Joseph2202HF/linkora.git
cd linkora
bash install.sh
# Choisissez l'option 2 ou 3 pour développement
```

### Tester les changements
```bash
# Terminal 1 : serveur
linkora --server

# Terminal 2 : client
linkora --client fichier.txt

# Ou directement
./bin/linkora --server
./bin/linkora --client fichier.txt
```

### Vérifier le format
Le code doit être lisible et bien commenté. Essayez de suivre le style existant.

## Structure du projet

```
linkora/
├── main.py              # Point d'entrée principal
├── install.sh           # Script d'installation
├── bin/
│   └── linkora          # Script wrapper Bash
├── core/
│   ├── client.py        # Logique client pour envoyer les fichiers
│   └── server.py        # Logique serveur pour recevoir les fichiers
├── utils/
│   └── config.py        # Configuration (HOST, PORT, BUFFER_SIZE)
├── README.md            # Documentation générale
├── CONTRIBUTING.md      # Ce fichier
├── LICENSE              # Licence MIT
└── .gitignore           # Fichiers ignorés par Git
```

### Descriptions des fichiers

- **main.py** : Gère les arguments CLI (`--server`, `--client`). À ne pas modifier sans raison valide.
- **core/client.py** : Client TCP qui envoie des fichiers. Améliorer l'affichage de progression ou ajouter de la validation.
- **core/server.py** : Serveur TCP qui reçoit des fichiers. Support pour plusieurs connexions serait bienvenue.
- **utils/config.py** : Centralise les paramètres réseau. Facile à configurer.

## Guidelines

### Code
- Utilisez Python 3.6+
- Nommez les variables et fonctions de façon claire
- Ajoutez des commentaires pour le code complexe
- Respectez l'indentation (4 espaces)

### Commits
- Messages clairs et en français ou anglais
- Un commit = une logique/feature
- Exemple : `git commit -m "Ajout affichage progression transfert"`

### Pull Requests
- Titre descriptif
- Description claire des changements
- Référrez les issues connexes : `Closes #123`
- Attendez la review avant de merger

## Idées de contributions bienvenues

- ✅ Ajout de gestion d'erreurs robustes
- ✅ Support de plusieurs connexions simultanées (threading/asyncio)
- ✅ Affichage de la barre de progression
- ✅ Compression des fichiers
- ✅ Chiffrement en transit
- ✅ Logging structuré
- ✅ Tests unitaires
- ✅ Documentation améliorée

## Questions ?

Ouvrez une discussion dans les [Issues](https://github.com/Joseph2202HF/linkora/issues) ou contactez les mainteneurs.

Merci de contribuer ! 🚀
