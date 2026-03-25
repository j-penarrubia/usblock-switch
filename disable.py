import subprocess
import sys
import winreg


def run_command(command, silent=False):
    out = subprocess.DEVNULL if silent else None
    completed = subprocess.run(command, shell=True, stdout=out, stderr=out)
    if completed.returncode != 0:
        print(f"Error ejecutando: {command}")
        sys.exit(1)


def disable_autoplay():
    powershell = (
        r'Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\AutoplayHandlers" '
        r'-Name "DisableAutoplay" -Value 1; '
        r'Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\AutoplayHandlers" '
        r'-Name "AutoplayHandlersVersion" -Value 2'
    )
    run_command(f'powershell -Command "{powershell}"', silent=True)
    print("Reproducción automática desactivada.")


def disable_usb_indexing():
    key_path = r"SOFTWARE\Policies\Microsoft\Windows\Windows Search"
    try:
        key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "DisableRemovableDriveIndexing", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
        print("Indexación de unidades USB desactivada.")
    except Exception as e:
        print(f"Error cambiando el registro: {e}")


def disable_storage_service():
    run_command(r'sc stop "StorSvc"', silent=True)
    run_command(r'sc config "StorSvc" start= disabled', silent=True)
    print("Servicio de almacenamiento desactivado.")


def disable_auto_mount():
    powershell = (
        r'Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\MountMgr" '
        r'-Name "NoAutoMount" -Value 1'
    )
    run_command(f'powershell -Command "{powershell}"', silent=True)
    print("Montaje automático de unidades desactivado.")


if __name__ == "__main__":
    if not sys.platform.startswith("win"):
        print("Este script solo funciona en Windows.")
        sys.exit(1)
    disable_autoplay()
    disable_usb_indexing()
    disable_storage_service()
    disable_auto_mount()
    print("\nAutomontaje de USB desactivado. Reinicia el equipo para aplicar los cambios.")