import os
import time
import sys
import signal
import random
import subprocess
import threading
import ctypes
import requests
import base64
from datetime import datetime

# Configuration GitHub
GITHUB_REPO = "A0095/Protection-"  # Nom du dépôt
GITHUB_FILE_PATH = "logs/logprotec.txt"  # Fichier distant dans le dépôt
GITHUB_TOKEN = "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"  # Remplace par ton token GitHub
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}"

def log_connection(status):
    log_folder = os.path.join(os.path.expanduser("~"), "Documents", "ScriptLogs")
    log_file = os.path.join(log_folder, "log.txt")
    
    if not os.path.exists(log_folder):
        os.makedirs(log_folder, exist_ok=True)
    
    with open(log_file, "a", encoding="utf-8") as file:
        file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {status}\n")
    
    upload_logs_to_github(log_file)  # Envoi automatique sur GitHub

def upload_logs_to_github(log_file):
    try:
        with open(log_file, "r", encoding="utf-8") as file:
            content = file.read()
        encoded_content = base64.b64encode(content.encode()).decode()
        
        # Vérifier si le fichier existe déjà sur GitHub
        response = requests.get(GITHUB_API_URL, headers={"Authorization": f"token {GITHUB_TOKEN}"})
        
        if response.status_code == 200:
            sha = response.json()["sha"]  # Le fichier existe déjà
        elif response.status_code == 404:
            print("Le fichier de logs n'existe pas, il sera créé.")
            sha = None  # Le fichier n'existe pas encore
        else:
            print("Erreur lors de la vérification du fichier GitHub :", response.json())
            return
        
        data = {
            "message": "Mise à jour des logs",
            "content": encoded_content,
            "branch": "main"
        }
        
        if sha:
            data["sha"] = sha  # Ajout du SHA si le fichier existe déjà
        
        response = requests.put(GITHUB_API_URL, json=data, headers={"Authorization": f"token {GITHUB_TOKEN}"})
        if response.status_code in [200, 201]:
            print("Logs envoyés sur GitHub avec succès !")
        else:
            print("Erreur lors de l'envoi des logs sur GitHub :", response.json())
    except Exception as e:
        print("Erreur lors de l'envoi des logs :", e)

def handle_exit(signum, frame):
    print("Fermeture détectée ! Arrêt de l'ordinateur...")
    log_connection("Le script a été fermé de force. Arrêt en cours...")
    print("Simulation : Arrêt de l'ordinateur désactivé pour test.")

def force_shutdown(stop_event):
    time.sleep(5)
    if not stop_event.is_set():
        print("Temps écoulé sans saisie ! Arrêt de l'ordinateur...")
        log_connection("Temps écoulé, arrêt de l'ordinateur.")
        print("simulation de coupure") 

def set_window_topmost():
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd:
        ctypes.windll.user32.SetForegroundWindow(hwnd)
        ctypes.windll.user32.ShowWindow(hwnd, 5)

def request_password():
    correct_password = "123"
    print("Veuillez entrer le mot de passe dans les 5 secondes :")
    
    stop_event = threading.Event()
    shutdown_thread = threading.Thread(target=force_shutdown, args=(stop_event,))
    shutdown_thread.start()
    
    set_window_topmost()
    
    start_time = time.time()
    while time.time() - start_time < 5:
        entered_password = input("Mot de passe : ")
        if entered_password == correct_password:
            print("Accès autorisé.")
            log_connection("Connexion réussie. Accès autorisé.")
            stop_event.set()
            return
        else:
            print("Mot de passe incorrect.")
    
    taunts = [
        "Pathétique. Même avec du temps, tu n'es capable de rien !",
        "Regarde-toi... un échec complet. Laisse tomber !",
        "Tu viens de prouver à quel point tu es incompétent. Dégage !"
    ]
    
    print(random.choice(taunts))
    print("Arrêt de l'ordinateur...")
    log_connection("Échec de l'authentification. Arrêt de l'ordinateur.")
    os.system("shutdown /s /t 1")

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)
    
    log_connection("Le script a été lancé.")
    request_password()
