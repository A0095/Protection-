import os
import time
import sys
import signal
import random
import subprocess
import threading
import ctypes
from datetime import datetime

def log_connection():
    documents_path = os.path.join(os.path.expanduser("~"), "Documents")
    log_file = os.path.join(documents_path, "connection_log.txt")
    
    if not os.path.exists(documents_path):
        os.makedirs(documents_path, exist_ok=True)
    
    with open(log_file, "a", encoding="utf-8") as file:
        file.write(f"Connexion détectée : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

def handle_exit(signum, frame):
    print("Fermeture détectée ! Arrêt de l'ordinateur...")
    os.system("shutdown /s /t 1")  # Commande d'arrêt de l'ordinateur pour Windows
    # os.system("sudo shutdown -h now")  # Commande pour Linux

def force_shutdown(stop_event):
    time.sleep(5)
    if not stop_event.is_set():
        print("Temps écoulé sans saisie ! Arrêt de l'ordinateur...")
        os.system("shutdown /s /t 1")  # Arrêt de l'ordinateur

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
    ]
    
    print(random.choice(taunts))
    print("Arrêt de l'ordinateur...")
    os.system("shutdown /s /t 1")  # Arrêt de l'ordinateur

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_exit)  # Capture Ctrl+C
    signal.signal(signal.SIGTERM, handle_exit)  # Capture la fermeture du processus
    
    log_connection()
    request_password()
