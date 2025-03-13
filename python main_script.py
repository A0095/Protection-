import os
import time
import sys
import signal
import random
import subprocess
import threading
import ctypes
from datetime import datetime

def log_connection(status):
    log_folder = os.path.join(os.path.expanduser("~"), "Documents", "ScriptLogs")
    log_file = os.path.join(log_folder, "logprotec.txt")
    
    if not os.path.exists(log_folder):
        os.makedirs(log_folder, exist_ok=True)
    
    with open(log_file, "a", encoding="utf-8") as file:
        file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {status}\n")

def handle_exit(signum, frame):
    print("Fermeture détectée ! Arrêt de l'ordinateur...")
    log_connection("Le script a été fermé de force. Arrêt en cours...")
    print("Simulation : Arrêt de l'ordinateur désactivé pour test.")

def force_shutdown(stop_event):
    time.sleep(5)
    if not stop_event.is_set():
        print("Temps écoulé sans saisie ! Arrêt de l'ordinateur...")
        log_connection("Temps écoulé, arrêt de l'ordinateur.")
        os.system("shutdown /s /t 1")

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
