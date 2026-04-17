#!/usr/bin/env python3
"""
Client Linkora - Transfert de fichiers optimisé
Découverte automatique et envoi haute performance avec progression moderne
"""

import socket
import struct
import os
import time
import sys
from pathlib import Path

# Import de la configuration
try:
    from utils.config import PORT, DISCOVERY_PORT, BUFFER_SIZE, DISCOVERY_TIMEOUT, PROGRESS_UPDATE_INTERVAL
except ImportError:
    PORT = 2026
    DISCOVERY_PORT = 2027
    BUFFER_SIZE = 4 * 1024 * 1024  # 4 Mo
    DISCOVERY_TIMEOUT = 3
    PROGRESS_UPDATE_INTERVAL = 5

# Constantes du protocole
DISCOVERY_MESSAGE = b"DISCOVER_LINKORA"
DISCOVERY_RESPONSE_PREFIX = "LINKORA:"

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

class FileSender:
    """Gestionnaire optimisé d'envoi de fichiers"""
    
    def __init__(self, host, port, filename):
        self.host = host
        self.port = port
        self.filename = Path(filename)
        self.start_time = None
        self.file_size = 0
        self.last_update = 0
        self.update_interval = 0.1  # 10 fps max
        
    def validate_file(self):
        """Vérifie que le fichier existe et est lisible"""
        if not self.filename.exists():
            raise FileNotFoundError(f"Fichier introuvable: {self.filename}")
        if not self.filename.is_file():
            raise ValueError(f"Ce n'est pas un fichier: {self.filename}")
        
        self.file_size = self.filename.stat().st_size
        if self.file_size == 0:
            raise ValueError("Le fichier est vide")
        
        return True
    
    def send(self):
        """Envoie le fichier au serveur"""
        self.start_time = time.time()
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, BUFFER_SIZE)
            sock.settimeout(30)
            
            print(f"{Colors.CYAN}🔗 Connexion à {self.host}:{self.port}...{Colors.ENDC}")
            
            try:
                sock.connect((self.host, self.port))
            except socket.timeout:
                raise ConnectionError(f"Timeout lors de la connexion à {self.host}:{self.port}")
            except ConnectionRefusedError:
                raise ConnectionError(f"Connexion refusée par {self.host}:{self.port}")
            
            print(f"{Colors.GREEN}✅ Connecté au serveur !{Colors.ENDC}")
            
            self._send_metadata(sock)
            self._send_file_content(sock)
            self._print_stats()
    
    def _send_metadata(self, sock):
        """Envoie les métadonnées du fichier"""
        filename_bytes = self.filename.name.encode('utf-8')
        
        sock.sendall(struct.pack('!H', len(filename_bytes)))
        sock.sendall(filename_bytes)
        sock.sendall(struct.pack('!Q', self.file_size))
        
        print(f"{Colors.BOLD}📄 Fichier: {self.filename.name}{Colors.ENDC}")
        print(f"{Colors.BOLD}📏 Taille: {self.file_size / 1024 / 1024:.2f} Mo{Colors.ENDC}")
    
    def _send_file_content(self, sock):
        """Envoie le contenu du fichier avec une barre de progression moderne"""
        sent = 0
        buffer_size = BUFFER_SIZE
        
        print(f"\n{Colors.CYAN}╭─────────────────────────────────────────────────────────╮{Colors.ENDC}")
        print(f"{Colors.CYAN}│{Colors.ENDC} {Colors.BOLD}ENVOI DU FICHIER{Colors.ENDC}".ljust(68) + f"{Colors.CYAN}│{Colors.ENDC}")
        print(f"{Colors.CYAN}├─────────────────────────────────────────────────────────┤{Colors.ENDC}")
        
        with open(self.filename, 'rb', buffering=buffer_size) as f:
            while True:
                data = f.read(buffer_size)
                if not data:
                    break
                
                sock.sendall(data)
                sent += len(data)
                
                current_time = time.time()
                if current_time - self.last_update >= self.update_interval:
                    self._print_progress_bar(sent, self.file_size)
                    self.last_update = current_time
        
        # Affichage final à 100%
        self._print_progress_bar(self.file_size, self.file_size)
        print(f"\n{Colors.CYAN}╰─────────────────────────────────────────────────────────╯{Colors.ENDC}")
    
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
        progress_line = f"\r{Colors.CYAN}│{Colors.ENDC} 📤 [{bar}] {percent:5.1f}% | {Colors.GREEN}{speed:6.2f} Mo/s{Colors.ENDC} | {current_mb:7.1f}/{total_mb:7.1f} Mo | ⏱️ {remaining_str:10s}"
        
        # Efface le reste de la ligne et affiche
        sys.stdout.write('\033[K' + progress_line)
        sys.stdout.flush()
    
    def _print_stats(self):
        """Affiche les statistiques finales"""
        elapsed = time.time() - self.start_time
        avg_speed = self.file_size / elapsed / 1024 / 1024 if elapsed > 0 else 0
        
        print(f"\n{Colors.GREEN}✅ Transfert terminé en {elapsed:.2f}s{Colors.ENDC}")
        print(f"{Colors.CYAN}🚀 Vitesse moyenne: {avg_speed:.2f} Mo/s{Colors.ENDC}")
        print(f"{Colors.CYAN}💾 Données envoyées: {self.file_size / 1024 / 1024:.2f} Mo{Colors.ENDC}")

class ServerDiscovery:
    """Gestionnaire de découverte de serveurs Linkora"""
    
    def __init__(self, timeout=DISCOVERY_TIMEOUT, discovery_port=DISCOVERY_PORT):
        self.timeout = timeout
        self.discovery_port = discovery_port
        self.discovered_servers = []
    
    def discover(self):
        """Découvre les serveurs Linkora sur le réseau"""
        print(f"{Colors.CYAN}🔍 Recherche de serveurs Linkora...{Colors.ENDC}")
        
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.settimeout(0.5)
            
            try:
                sock.sendto(DISCOVERY_MESSAGE, ("255.255.255.255", self.discovery_port))
            except PermissionError:
                print(f"{Colors.YELLOW}⚠️  Permission refusée pour le broadcast{Colors.ENDC}")
                return []
            except Exception as e:
                print(f"{Colors.YELLOW}⚠️  Erreur d'envoi broadcast: {e}{Colors.ENDC}")
                return []
            
            start_time = time.time()
            
            while time.time() - start_time < self.timeout:
                try:
                    data, addr = sock.recvfrom(1024)
                    payload = data.decode('utf-8', errors='ignore')
                    
                    if payload.startswith(DISCOVERY_RESPONSE_PREFIX):
                        server_info = self._parse_response(payload, addr)
                        if server_info:
                            self.discovered_servers.append(server_info)
                            print(f"{Colors.GREEN}✨ Serveur trouvé: {server_info['host']}:{server_info['port']}{Colors.ENDC}")
                            
                except socket.timeout:
                    continue
                except Exception:
                    continue
        
        return self.discovered_servers
    
    def _parse_response(self, payload, addr):
        """Parse la réponse du serveur"""
        parts = payload.split(":")
        if len(parts) >= 3:
            try:
                port = int(parts[2])
                version = int(parts[3][1:]) if len(parts) > 3 and parts[3].startswith('v') else 1
                
                return {
                    'host': parts[1],
                    'port': port,
                    'version': version,
                    'addr': addr
                }
            except (ValueError, IndexError):
                pass
        return None
    
    def get_best_server(self):
        """Retourne le meilleur serveur disponible"""
        if not self.discovered_servers:
            return None
        
        local_ip = self._get_local_ip()
        local_prefix = '.'.join(local_ip.split('.')[:3])
        
        for server in self.discovered_servers:
            if server['host'].startswith(local_prefix):
                return server
        
        return self.discovered_servers[0]
    
    def _get_local_ip(self):
        """Obtient l'adresse IP locale"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.connect(("8.8.8.8", 80))
                return sock.getsockname()[0]
        except Exception:
            return "127.0.0.1"

def run_client(filename=None, no_discover=False):
    """Point d'entrée principal du client"""
    
    print(f"\n{Colors.BOLD}{Colors.GREEN}╔══════════════════════════════════════════════════════════╗{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.GREEN}║{Colors.ENDC}           📤 CLIENT LINKORA                               {Colors.BOLD}{Colors.GREEN}║{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.GREEN}╚══════════════════════════════════════════════════════════╝{Colors.ENDC}")
    
    if no_discover:
        print(f"{Colors.YELLOW}🔍 Mode découverte désactivé{Colors.ENDC}")
        print(f"{Colors.CYAN}📝 Configuration manuelle requise{Colors.ENDC}")
        
        if not filename:
            filename = input(f"{Colors.CYAN}📁 Chemin du fichier à envoyer: {Colors.ENDC}").strip()
            if not filename:
                print(f"{Colors.RED}❌ Aucun fichier spécifié{Colors.ENDC}")
                return
        
        host = input(f"{Colors.CYAN}🌐 Adresse IP du serveur: {Colors.ENDC}").strip()
        if not host:
            print(f"{Colors.RED}❌ Adresse IP requise{Colors.ENDC}")
            return
            
        try:
            port_input = input(f"{Colors.CYAN}🔌 Port du serveur [{PORT}]: {Colors.ENDC}").strip()
            port = int(port_input) if port_input else PORT
        except ValueError:
            print(f"{Colors.YELLOW}⚠️  Port invalide, utilisation du port {PORT}{Colors.ENDC}")
            port = PORT
        
        try:
            sender = FileSender(host, port, filename)
            sender.validate_file()
            sender.send()
        except FileNotFoundError as e:
            print(f"{Colors.RED}❌ {e}{Colors.ENDC}")
        except ValueError as e:
            print(f"{Colors.RED}❌ {e}{Colors.ENDC}")
        except ConnectionError as e:
            print(f"{Colors.RED}❌ {e}{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.RED}❌ Erreur lors du transfert: {e}{Colors.ENDC}")
        return
    
    if filename:
        filepath = Path(filename)
        if not filepath.exists():
            print(f"{Colors.RED}❌ Fichier introuvable: {filename}{Colors.ENDC}")
            return
        if not filepath.is_file():
            print(f"{Colors.RED}❌ Ce n'est pas un fichier: {filename}{Colors.ENDC}")
            return
    
    discovery = ServerDiscovery()
    servers = discovery.discover()
    
    if not servers:
        print(f"\n{Colors.RED}❌ Aucun serveur Linkora trouvé sur le réseau{Colors.ENDC}")
        print(f"{Colors.YELLOW}💡 Vérifiez que:{Colors.ENDC}")
        print(f"   1. Un serveur est en cours d'exécution")
        print(f"   2. Vous êtes sur le même réseau")
        print(f"   3. Le port UDP {DISCOVERY_PORT} n'est pas bloqué")
        print(f"\n{Colors.CYAN}📝 Ou utilisez --no-discover pour vous connecter manuellement{Colors.ENDC}")
        return
    
    if len(servers) > 1:
        print(f"\n{Colors.CYAN}📡 {len(servers)} serveurs trouvés:{Colors.ENDC}")
        for i, server in enumerate(servers):
            print(f"   {i+1}. {server['host']}:{server['port']}")
        
        best = discovery.get_best_server()
        if best:
            print(f"\n{Colors.GREEN}💡 Serveur recommandé: {best['host']}:{best['port']} (même sous-réseau){Colors.ENDC}")
        
        try:
            choice = input(f"\n{Colors.CYAN}🔢 Choisissez un serveur (numéro) ou Entrée pour le premier: {Colors.ENDC}").strip()
            if choice:
                idx = int(choice) - 1
                server = servers[idx]
            else:
                server = best or servers[0]
        except (ValueError, IndexError):
            print(f"{Colors.YELLOW}⚠️  Choix invalide, utilisation du serveur recommandé{Colors.ENDC}")
            server = best or servers[0]
    else:
        server = servers[0]
    
    print(f"\n{Colors.GREEN}🎯 Serveur sélectionné: {server['host']}:{server['port']}{Colors.ENDC}")
    
    if not filename:
        filename = input(f"\n{Colors.CYAN}📁 Chemin du fichier à envoyer: {Colors.ENDC}").strip()
        if not filename:
            print(f"{Colors.RED}❌ Aucun fichier spécifié{Colors.ENDC}")
            return
    
    try:
        sender = FileSender(server['host'], server['port'], filename)
        sender.validate_file()
        sender.send()
        
    except FileNotFoundError as e:
        print(f"{Colors.RED}❌ {e}{Colors.ENDC}")
    except ValueError as e:
        print(f"{Colors.RED}❌ {e}{Colors.ENDC}")
    except ConnectionRefusedError:
        print(f"{Colors.RED}❌ Connexion refusée par {server['host']}:{server['port']}{Colors.ENDC}")
    except socket.timeout:
        print(f"{Colors.RED}❌ Timeout lors de la connexion à {server['host']}:{server['port']}{Colors.ENDC}")
    except ConnectionError as e:
        print(f"{Colors.RED}❌ {e}{Colors.ENDC}")
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️  Transfert interrompu par l'utilisateur{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.RED}❌ Erreur lors du transfert: {e}{Colors.ENDC}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] in ["--no-discover", "-n"]:
            filename = sys.argv[2] if len(sys.argv) > 2 else None
            run_client(filename=filename, no_discover=True)
        else:
            run_client(filename=sys.argv[1])
    else:
        run_client()