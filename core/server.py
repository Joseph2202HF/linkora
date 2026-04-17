#!/usr/bin/env python3
"""
Serveur Linkora - Transfert de fichiers optimisé
Performances maximales avec buffer de 4 Mo et progression moderne
"""

import socket
import struct
import threading
import os
import time
import sys
from pathlib import Path

# Import de la configuration
try:
    from utils.config import SERVER_HOST, PORT, DISCOVERY_PORT, BUFFER_SIZE, PROGRESS_UPDATE_INTERVAL
except ImportError:
    SERVER_HOST = "0.0.0.0"
    PORT = 2026
    DISCOVERY_PORT = 2027
    BUFFER_SIZE = 4 * 1024 * 1024  # 4 Mo
    PROGRESS_UPDATE_INTERVAL = 5

# Constantes du protocole
DISCOVERY_MESSAGE = b"DISCOVER_LINKORA"
DISCOVERY_RESPONSE_PREFIX = b"LINKORA:"
PROTOCOL_VERSION = 1

# Couleurs ANSI pour le terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class FileReceiver:
    """Gestionnaire optimisé de réception de fichiers"""
    
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.start_time = time.time()
        self.last_update = 0
        self.update_interval = 0.1  # 10 fps max
        
    def receive_metadata(self):
        """Reçoit et valide les métadonnées du fichier"""
        name_len_data = self._recv_exact(2)
        name_len = struct.unpack('!H', name_len_data)[0]
        
        if name_len > 255:
            raise ValueError(f"Nom de fichier trop long: {name_len} caractères")
            
        filename = self._recv_exact(name_len).decode('utf-8', errors='strict')
        safe_filename = Path(filename).name
        
        if not safe_filename or safe_filename.startswith('.'):
            safe_filename = f"received_file_{int(time.time())}"
            
        size_data = self._recv_exact(8)
        file_size = struct.unpack('!Q', size_data)[0]
        
        return safe_filename, file_size
    
    def _recv_exact(self, count):
        """Reçoit exactement count octets (optimisé)"""
        data = bytearray()
        while len(data) < count:
            chunk = self.conn.recv(min(count - len(data), 65536))
            if not chunk:
                raise ConnectionError("Connexion interrompue")
            data.extend(chunk)
        return bytes(data)
    
    def receive_file(self, filename, total_size):
        """Reçoit le fichier avec une barre de progression moderne"""
        received = 0
        buffer_size = BUFFER_SIZE
        
        print(f"\n{Colors.CYAN}╭─────────────────────────────────────────────────────────╮{Colors.ENDC}")
        print(f"{Colors.CYAN}│{Colors.ENDC} {Colors.BOLD}RÉCEPTION DU FICHIER{Colors.ENDC}".ljust(68) + f"{Colors.CYAN}│{Colors.ENDC}")
        print(f"{Colors.CYAN}├─────────────────────────────────────────────────────────┤{Colors.ENDC}")
        
        with open(filename, 'wb', buffering=buffer_size) as f:
            while received < total_size:
                chunk_size = min(buffer_size, total_size - received)
                
                try:
                    data = self.conn.recv(chunk_size)
                except socket.timeout:
                    continue
                    
                if not data:
                    break
                
                f.write(data)
                received += len(data)
                
                current_time = time.time()
                if current_time - self.last_update >= self.update_interval:
                    self._print_progress_bar(received, total_size)
                    self.last_update = current_time
        
        # Affichage final à 100%
        self._print_progress_bar(total_size, total_size)
        print(f"\n{Colors.CYAN}╰─────────────────────────────────────────────────────────╯{Colors.ENDC}")
        
        return received == total_size
    
    def _print_progress_bar(self, current, total):
        """Affiche une barre de progression moderne et colorée"""
        percent = (current * 100) / total
        elapsed = time.time() - self.start_time
        speed = current / elapsed / 1024 / 1024 if elapsed > 0 else 0
        
        # Estimation du temps restant
        if speed > 0:
            remaining_seconds = (total - current) / (speed * 1024 * 1024)
            if remaining_seconds > 60:
                remaining_str = f"{int(remaining_seconds // 60)}m{int(remaining_seconds % 60):02d}s"
            else:
                remaining_str = f"{remaining_seconds:.0f}s"
        else:
            remaining_str = "calcul..."
        
        # Création de la barre de progression
        bar_length = 30
        filled_length = int(bar_length * current // total)
        
        # Dégradé de couleurs selon la progression
        if percent < 33:
            bar_color = Colors.RED
        elif percent < 66:
            bar_color = Colors.YELLOW
        else:
            bar_color = Colors.GREEN
        
        # Barre avec caractères Unicode
        bar_filled = '█' * filled_length
        bar_empty = '░' * (bar_length - filled_length)
        bar = f"{bar_color}{bar_filled}{Colors.ENDC}{bar_empty}"
        
        # Formatage des tailles
        current_mb = current / 1024 / 1024
        total_mb = total / 1024 / 1024
        
        # Ligne de progression moderne
        progress_line = f"\r{Colors.CYAN}│{Colors.ENDC} 📥 [{bar}] {percent:5.1f}% | {Colors.GREEN}{speed:6.2f} Mo/s{Colors.ENDC} | {current_mb:7.1f}/{total_mb:7.1f} Mo | ⏱️ {remaining_str:10s}"
        
        # Efface le reste de la ligne et affiche
        sys.stdout.write('\033[K' + progress_line)
        sys.stdout.flush()
    
    def get_stats(self, total_size):
        """Affiche les statistiques finales du transfert"""
        elapsed = time.time() - self.start_time
        avg_speed = total_size / elapsed / 1024 / 1024 if elapsed > 0 else 0
        
        print(f"\n{Colors.GREEN}✅ Transfert terminé en {elapsed:.2f}s{Colors.ENDC}")
        print(f"{Colors.CYAN}📊 Vitesse moyenne: {avg_speed:.2f} Mo/s{Colors.ENDC}")
        print(f"{Colors.CYAN}💾 Taille totale: {total_size / 1024 / 1024:.2f} Mo{Colors.ENDC}")

def get_local_ip():
    """Obtient l'adresse IP locale de manière fiable"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(("8.8.8.8", 80))
            return sock.getsockname()[0]
    except Exception:
        try:
            hostname = socket.gethostname()
            return socket.gethostbyname(hostname)
        except Exception:
            return "127.0.0.1"

def discovery_responder(host, port, discovery_port):
    """Thread de réponse aux découvertes UDP"""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        try:
            sock.bind(("", discovery_port))
        except OSError:
            print(f"{Colors.YELLOW}⚠️  Port de découverte {discovery_port} déjà utilisé{Colors.ENDC}")
            return
            
        response = f"LINKORA:{host}:{port}:v{PROTOCOL_VERSION}".encode('utf-8')
        
        print(f"{Colors.GREEN}🔍 Service de découverte actif sur UDP:{discovery_port}{Colors.ENDC}")
        
        while True:
            try:
                data, addr = sock.recvfrom(1024)
                if data == DISCOVERY_MESSAGE:
                    sock.sendto(response, addr)
            except Exception:
                continue

def handle_client(conn, addr):
    """Gère une connexion client individuelle"""
    try:
        conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        conn.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFFER_SIZE)
        
        receiver = FileReceiver(conn, addr)
        
        filename, file_size = receiver.receive_metadata()
        print(f"{Colors.BOLD}📄 Réception de: {filename}{Colors.ENDC}")
        print(f"{Colors.BOLD}📏 Taille attendue: {file_size / 1024 / 1024:.2f} Mo{Colors.ENDC}")
        
        success = receiver.receive_file(filename, file_size)
        
        if success:
            receiver.get_stats(file_size)
            print(f"{Colors.GREEN}✅ Fichier '{filename}' reçu avec succès{Colors.ENDC}")
        else:
            print(f"{Colors.YELLOW}⚠️  Transfert incomplet pour '{filename}'{Colors.ENDC}")
            
    except struct.error as e:
        print(f"{Colors.RED}❌ Erreur de protocole avec {addr}: {e}{Colors.ENDC}")
    except UnicodeDecodeError as e:
        print(f"{Colors.RED}❌ Erreur d'encodage avec {addr}: {e}{Colors.ENDC}")
    except ConnectionError as e:
        print(f"{Colors.RED}❌ Connexion perdue avec {addr}: {e}{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.RED}❌ Erreur avec le client {addr}: {e}{Colors.ENDC}")
    finally:
        conn.close()
        print(f"{Colors.CYAN}{'─'*58}{Colors.ENDC}")

def run_server(host=None, port=None):
    """Point d'entrée principal du serveur"""
    host = host or SERVER_HOST
    port = port or PORT
    
    local_ip = get_local_ip() if host in ("0.0.0.0", "", None) else host
    
    discovery_thread = threading.Thread(
        target=discovery_responder,
        args=(local_ip, port, DISCOVERY_PORT),
        daemon=True,
        name="DiscoveryService"
    )
    discovery_thread.start()
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((host, port))
        server.listen(5)
        
        print(f"\n{Colors.BOLD}{Colors.GREEN}╔══════════════════════════════════════════════════════════╗{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.GREEN}║{Colors.ENDC}           🚀 SERVEUR LINKORA DÉMARRÉ                       {Colors.BOLD}{Colors.GREEN}║{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.GREEN}╚══════════════════════════════════════════════════════════╝{Colors.ENDC}")
        print(f"{Colors.CYAN}🌐 Adresse: {local_ip}:{port}{Colors.ENDC}")
        print(f"{Colors.CYAN}📦 Buffer: {BUFFER_SIZE / 1024 / 1024:.0f} Mo{Colors.ENDC}")
        print(f"{Colors.CYAN}⏳ En attente de connexion...{Colors.ENDC}")
        print(f"{Colors.CYAN}{'─'*58}{Colors.ENDC}")
        
        while True:
            try:
                conn, addr = server.accept()
                print(f"\n{Colors.GREEN}🔗 Client connecté: {addr[0]}:{addr[1]}{Colors.ENDC}")
                
                client_thread = threading.Thread(
                    target=handle_client,
                    args=(conn, addr),
                    daemon=True
                )
                client_thread.start()
                
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}🛑 Arrêt du serveur...{Colors.ENDC}")
                break
            except Exception as e:
                print(f"{Colors.RED}❌ Erreur d'acceptation: {e}{Colors.ENDC}")
                
    except PermissionError:
        print(f"{Colors.RED}❌ Permission refusée pour le port {port}{Colors.ENDC}")
        print(f"{Colors.YELLOW}💡 Essayez un port > 1024 ou exécutez avec les droits administrateur{Colors.ENDC}")
    except OSError as e:
        print(f"{Colors.RED}❌ Erreur réseau: {e}{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.RED}❌ Erreur fatale du serveur: {e}{Colors.ENDC}")
    finally:
        server.close()
        print(f"{Colors.CYAN}👋 Serveur arrêté{Colors.ENDC}")

if __name__ == "__main__":
    try:
        run_server()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}👋 Arrêt demandé par l'utilisateur{Colors.ENDC}")