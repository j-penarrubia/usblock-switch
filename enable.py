import subprocess
import sys
import winreg


def run_command(command, silent=False):
    out = subprocess.DEVNULL if silent else None
    completed = subprocess.run(command, shell=True, stdout=out, stderr=out)
    if completed.returncode != 0:
        print(f"Error ejecutando: {command}")
        sys.exit(1)


def restore_autoplay():
    powershell = (
        r'Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\AutoplayHandlers" '
        r'-Name "DisableAutoplay" -Value 0; '
        r'Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\AutoplayHandlers" '
        r'-Name "AutoplayHandlersVersion" -Value 2'
    )
    run_command(f'powershell -Command "{powershell}"', silent=True)
    print("Reproducción automática activada.")


def restore_usb_indexing():
    key_path = r"SOFTWARE\Policies\Microsoft\Windows\Windows Search"
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "DisableRemovableDriveIndexing", 0, winreg.REG_DWORD, 0)
        winreg.CloseKey(key)
        print("Indexación de unidades USB activada.")
    except Exception:
        print("La clave del registro no existe o ya estaba restablecida.")


def restore_storage_service():
    run_command(r'sc config "StorSvc" start= demand', silent=True)
    run_command(r'sc start "StorSvc"', silent=True)
    print("Servicio de almacenamiento activado.")


def restore_auto_mount():
    powershell = (
        r'Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\MountMgr" '
        r'-Name "NoAutoMount" -Value 0'
    )
    run_command(f'powershell -Command "{powershell}"', silent=True)
    print("Montaje automático de unidades activado.")


if __name__ == "__main__":
    if not sys.platform.startswith("win"):
        print("Este script solo funciona en Windows.")
        sys.exit(1)
    restore_autoplay()
    restore_usb_indexing()
    restore_storage_service()
    restore_auto_mount()
    print("\nAutomontaje de USB activado. Reinicia el equipo para aplicar los cambios.")
