import os
import time
import sys
import signal
import random
import subprocess
import requests
from datetime import datetime
import threading
import ctypes

def update_script():
    GITHUB_URL = "https://github.com/A0095/Protection-/new/main"
    LOCAL_SCRIPT_PATH = sys.argv[0]  # Chemin du script actuel
    
    try:
        response = requests.get(GITHUB_URL)
        if response.status_code == 200:
            with open(LOCAL_SCRIPT_PATH, "wb") as file:
                file.write(response.content)
            print("Mise à jour réussie ! Relance du script...")
            os.execv(sys.executable, [sys.executable] + sys.argv)  # Relance le script mis à jour
        else:
            print("Erreur lors du téléchargement de la mise à jour :", response.status_code)
    except Exception as e:
        print("Échec de la mise à jour :", e)

def log_connection():
    documents_path = os.path.join(os.path.expanduser("~"), "Documents")
    log_file = os.path.join(documents_path, "connection_log.txt")
    
    if not os.path.exists(documents_path):
        os.makedirs(documents_path, exist_ok=True)
    
    with open(log_file, "a", encoding="utf-8") as file:
        file.write(f"Connexion détectée : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

def handle_exit(signum, frame):
    print("Fermeture détectée ! (Simulation de l'arrêt de l'ordinateur)")

def force_shutdown(stop_event):
    time.sleep(5)
    if not stop_event.is_set():
        print("Temps écoulé sans saisie ! (Simulation de l'arrêt de l'ordinateur)")

def set_window_topmost():
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd:
        ctypes.windll.user32.SetForegroundWindow(hwnd)
        ctypes.windll.user32.ShowWindow(hwnd, 5)  # 5 = SW_SHOW

def request_password():
    correct_password = "123"  # Remplacez par le mot de passe souhaité
    print("Veuillez entrer le mot de passe dans les 5 secondes :")
    
    stop_event = threading.Event()
    shutdown_thread = threading.Thread(target=force_shutdown, args=(stop_event,))
    shutdown_thread.start()
    
    set_window_topmost()  # Maintient la fenêtre au premier plan
    
    start_time = time.time()
    while time.time() - start_time < 5:
        entered_password = input("Mot de passe : ")
        if entered_password == correct_password:
            print("Accès autorisé.")
            stop_event.set()  # Empêche l'arrêt de l'ordinateur
            return  # Arrête la fonction immédiatement
        else:
            print("Mot de passe incorrect.")
    
    taunts = [
        "Pathétique. Même avec du temps, tu n'es capable de rien !",
        "Regarde-toi... un échec complet. Laisse tomber !",
        "Tu viens de prouver à quel point tu es incompétent. Dégage !"
        "tes pas beau" 
    ]
    
    print(random.choice(taunts))
    print("(Simulation de l'arrêt de l'ordinateur)")

if __name__ == "__main__":
    update_script()  # Vérifie et met à jour le script avant exécution
    signal.signal(signal.SIGINT, handle_exit)  # Capture Ctrl+C
    signal.signal(signal.SIGTERM, handle_exit)  # Capture la fermeture du processus
    
    log_connection()
    request_password()
