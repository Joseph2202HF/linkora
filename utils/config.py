# Configuration réseau
SERVER_HOST = "0.0.0.0"
CLIENT_HOST = "127.0.0.1"
PORT = 2026
DISCOVERY_PORT = 2027

# Buffer optimisé pour les performances réseau
# 4 Mo est idéal pour saturer un réseau Gigabit sans surcharger la RAM
BUFFER_SIZE = 4 * 1024 * 1024  # 4 Mo

# Timeout pour la découverte (secondes)
DISCOVERY_TIMEOUT = 3

# Délai entre les mises à jour de progression (pourcentage)
PROGRESS_UPDATE_INTERVAL = 5  # Affiche tous les 5%