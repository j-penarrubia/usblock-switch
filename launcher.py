import ctypes
import sys
import os
import subprocess
import threading
import winreg
import tkinter as tk
from tkinter import scrolledtext

def resource_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    script = os.path.abspath(sys.argv[0])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}"', None, 1)
    sys.exit()

# --- Leer estado real del registro de Windows ---
def get_automount_status():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                             r"SYSTEM\CurrentControlSet\Services\MountMgr")
        value, _ = winreg.QueryValueEx(key, "NoAutoMount")
        winreg.CloseKey(key)
        return value == 0
    except FileNotFoundError:
        return True
    except Exception:
        return None

def update_status():
    status = get_automount_status()
    if status is True:
        status_label.config(text="  ●  Automontaje: ACTIVADO", fg="#00e676")
    elif status is False:
        status_label.config(text="  ●  Automontaje: DESACTIVADO", fg="#ff5252")
    else:
        status_label.config(text="  ●  Estado: desconocido", fg="#ffeb3b")

# --- Log en el widget de texto ---
def log(text):
    output_text.config(state="normal")
    output_text.insert(tk.END, text)
    output_text.see(tk.END)
    output_text.config(state="disabled")

# --- Ejecutar script y capturar output ---
def run_script(nombre):
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    ruta = os.path.join(base_dir, nombre)

    def execute():
        log(f"\n▶ Ejecutando {nombre}...\n")
        try:
            proc = subprocess.Popen(
                ["python", ruta],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            for line in proc.stdout:
                log(line)
            proc.wait()
            root.after(300, update_status)
        except Exception as e:
            log(f"✖ Error: {e}\n")

    threading.Thread(target=execute, daemon=True).start()

# ─────────────── GUI ───────────────
root = tk.Tk()
root.title("USB AutoMount Switch")
root.geometry("440x330")
root.resizable(False, False)
root.configure(bg="#1e1e2e")
root.iconbitmap(resource_path("usb.ico"))

tk.Label(root, text="USB AutoMount Switch",
         font=("Segoe UI", 12, "bold"),
         bg="#1e1e2e", fg="#cdd6f4").pack(pady=(12, 6))

btn_frame = tk.Frame(root, bg="#1e1e2e")
btn_frame.pack(pady=2)

tk.Button(btn_frame, text="⛔  Desactivar automontaje",
          width=22, bg="#c62828", fg="white",
          font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2",
          command=lambda: run_script("disable.py")).pack(side="left", padx=6)

tk.Button(btn_frame, text="✅  Activar automontaje",
          width=22, bg="#1565c0", fg="white",
          font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2",
          command=lambda: run_script("enable.py")).pack(side="left", padx=6)

output_text = scrolledtext.ScrolledText(
    root, height=10, width=56,
    bg="#11111b", fg="#a6e3a1",
    font=("Consolas", 9),
    state="disabled", relief="flat",
    insertbackground="#cdd6f4",
    wrap="word"
)
output_text.pack(padx=10, pady=(8, 0))

status_label = tk.Label(root,
    text="  ●  Comprobando estado...",
    font=("Segoe UI", 9, "bold"),
    bg="#181825", fg="#cdd6f4",
    anchor="w", padx=6)
status_label.pack(fill="x", side="bottom", ipady=5)

update_status()
root.mainloop()