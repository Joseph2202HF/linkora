#!/usr/bin/env python3
"""
Linkora - Système de transfert de fichiers haute performance
Point d'entrée principal avec interface en ligne de commande
"""

import argparse
import sys
import os
from pathlib import Path

# Import des modules core
from core import server as server_module
from core import client as client_module

# Information de version
__version__ = "2.0.0"
__author__ = "Linkora Team"

class LinkoraCLI:
    """Interface en ligne de commande pour Linkora"""
    
    def __init__(self):
        self.parser = self._create_parser()
        
    def _create_parser(self):
        """Crée le parseur d'arguments avec une interface riche"""
        
        # Parseur principal
        parser = argparse.ArgumentParser(
            prog="linkora",
            description="🔗 Linkora - Transfert de fichiers haute performance sur réseau local",
            epilog="Exemples:\n"
                   "  linkora --server              # Démarre le serveur\n"
                   "  linkora --client fichier.zip   # Envoie fichier.zip\n"
                   "  linkora -s -p 8080            # Serveur sur port 8080\n"
                   "  linkora -c fichier.txt --no-discover  # Mode manuel",
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        
        # Groupe principal (mutuellement exclusif)
        group = parser.add_mutually_exclusive_group(required=True)
        
        group.add_argument(
            "-s", "--server",
            action="store_true",
            help="🚀 Démarrer le serveur Linkora (mode réception)"
        )
        
        group.add_argument(
            "-c", "--client",
            type=str,
            metavar="FICHIER",
            help="📤 Envoyer un fichier vers un serveur Linkora"
        )
        
        # Options avancées
        parser.add_argument(
            "-H", "--host",
            type=str,
            help="Adresse IP spécifique pour le serveur (défaut: 0.0.0.0)"
        )
        
        parser.add_argument(
            "-p", "--port",
            type=int,
            help="Port personnalisé (défaut: 2026)"
        )
        
        parser.add_argument(
            "-v", "--version",
            action="version",
            version=f"Linkora v{__version__}",
            help="Afficher la version"
        )
        
        parser.add_argument(
            "--no-discover",
            action="store_true",
            help="Désactiver la découverte automatique (client uniquement)"
        )
        
        parser.add_argument(
            "-q", "--quiet",
            action="store_true",
            help="Mode silencieux (moins de messages)"
        )
        
        return parser
    
    def run(self, args=None):
        """Exécute la CLI avec les arguments donnés"""
        
        if args is None:
            args = sys.argv[1:]
            
        # Parse les arguments
        try:
            parsed_args = self.parser.parse_args(args)
        except SystemExit:
            return 1
            
        # Configuration du mode silencieux
        if parsed_args.quiet:
            self._enable_quiet_mode()
            
        # Exécution de la commande appropriée
        try:
            if parsed_args.server:
                return self._run_server(parsed_args)
            elif parsed_args.client:
                return self._run_client(parsed_args)
        except KeyboardInterrupt:
            print("\n⚠️  Opération interrompue par l'utilisateur")
            return 130
        except Exception as e:
            print(f"❌ Erreur: {e}")
            if not parsed_args.quiet:
                import traceback
                traceback.print_exc()
            return 1
            
        return 0
    
    def _run_server(self, args):
        """Lance le serveur avec les paramètres spécifiés"""
        
        print_banner("Serveur Linkora")
        
        # Préparation des paramètres
        host = args.host
        port = args.port
        
        # Validation du port
        if port and (port < 1024 or port > 65535):
            print("⚠️  Port invalide. Utilisation du port par défaut (2026)")
            port = None
            
        print(f"🌐 Configuration: {'Auto' if not host else host}:{port if port else 2026}")
        print()
        
        # Lancement du serveur
        try:
            server_module.run_server(host=host, port=port)
        except PermissionError:
            print("❌ Permission refusée. Essayez avec un port > 1024")
            return 1
        except OSError as e:
            print(f"❌ Erreur réseau: {e}")
            return 1
        except TypeError as e:
            print(f"❌ Erreur de paramètre: {e}")
            print("💡 Assurez-vous que run_server() accepte les arguments 'host' et 'port'")
            return 1
            
        return 0
    
    def _run_client(self, args):
        """Lance le client avec les paramètres spécifiés"""
        
        print_banner("Client Linkora")
        
        # Vérification du fichier
        filename = args.client
        filepath = Path(filename)
        
        if not filepath.exists():
            print(f"❌ Fichier introuvable: {filename}")
            return 1
            
        if not filepath.is_file():
            print(f"❌ Ce n'est pas un fichier: {filename}")
            return 1
            
        # Affichage des informations
        file_size = filepath.stat().st_size
        print(f"📁 Fichier: {filepath.name}")
        print(f"📏 Taille: {file_size / 1024 / 1024:.2f} Mo")
        
        if args.no_discover:
            print("🔍 Mode découverte désactivé")
            
        print()
        
        # Lancement du client
        try:
            client_module.run_client(
                filename=str(filepath.absolute()),
                no_discover=args.no_discover
            )
        except TypeError as e:
            print(f"❌ Erreur de paramètre: {e}")
            print("💡 Assurez-vous que run_client() accepte l'argument 'no_discover'")
            
            # Fallback : appel sans l'argument problématique
            print("🔄 Tentative avec les paramètres par défaut...")
            try:
                client_module.run_client(filename=str(filepath.absolute()))
            except Exception as e2:
                print(f"❌ Échec: {e2}")
                return 1
                
        except ConnectionError as e:
            print(f"❌ {e}")
            return 1
        except Exception as e:
            print(f"❌ Erreur lors du transfert: {e}")
            return 1
            
        return 0
    
    def _enable_quiet_mode(self):
        """Active le mode silencieux (réduction des logs)"""
        import logging
        logging.getLogger().setLevel(logging.WARNING)

def print_banner(title):
    """Affiche une bannière ASCII élégante"""
    banner = f"""
╔══════════════════════════════════════════════════════════╗
║                    🔗 LINKORA v{__version__}                     ║
║              Transfert de fichiers haute performance        ║
╚══════════════════════════════════════════════════════════╝
    {title.center(56)}
════════════════════════════════════════════════════════════
"""
    print(banner)

def main():
    """Point d'entrée principal"""
    
    # Configuration de l'encodage pour Windows
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except:
            pass
    
    # Création et exécution de la CLI
    cli = LinkoraCLI()
    exit_code = cli.run()
    
    sys.exit(exit_code)

# Point d'entrée pour setuptools
def entry_point():
    """Point d'entrée pour l'installation via pip"""
    main()

if __name__ == "__main__":
    main()