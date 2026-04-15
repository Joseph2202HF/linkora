#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LINKORA_BIN="$SCRIPT_DIR/bin/linkora"

if [ ! -f "$LINKORA_BIN" ]; then
  echo "Erreur : le script $LINKORA_BIN est introuvable."
  exit 1
fi

printf "Installer Linkora sur cette machine ?\n"
printf "1) Copier dans /usr/local/bin (recommandé, nécessite sudo)\n"
printf "2) Ajouter %s/bin au PATH dans votre shell\n" "$SCRIPT_DIR"
printf "3) Ne rien faire\n"
read -rp "Choix [1/2/3] : " choice

case "$choice" in
  1)
    sudo cp "$LINKORA_BIN" /usr/local/bin/linkora
    sudo chmod +x /usr/local/bin/linkora
    echo "Linkora installé dans /usr/local/bin/linkora"
    echo "Vous pouvez maintenant exécuter : linkora --server"
    ;;
  2)
    SHELL_NAME="$(basename "$SHELL")"
    if [[ "$SHELL_NAME" == "bash" ]]; then
      RC_FILE="$HOME/.bashrc"
    elif [[ "$SHELL_NAME" == "zsh" ]]; then
      RC_FILE="$HOME/.zshrc"
    else
      RC_FILE="$HOME/.profile"
    fi

    EXPORT_LINE="export PATH=\"$SCRIPT_DIR/bin:\\$PATH\""
    if grep -Fxq "$EXPORT_LINE" "$RC_FILE" 2>/dev/null; then
      echo "Le PATH est déjà configuré dans $RC_FILE"
    else
      echo "$EXPORT_LINE" >> "$RC_FILE"
      echo "Ajout de $SCRIPT_DIR/bin à PATH dans $RC_FILE"
      echo "Recommencez le terminal ou exécutez : source $RC_FILE"
    fi
    echo "Vous pouvez maintenant exécuter : linkora --server"
    ;;
  3)
    echo "Aucune modification effectuée."
    echo "Exécutez directement : $LINKORA_BIN --server"
    ;;
  *)
    echo "Choix invalide. Aucune action effectuée."
    exit 1
    ;;
esac
