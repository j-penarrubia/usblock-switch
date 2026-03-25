Write-Host "Comprobando dependencias..." -ForegroundColor Cyan

$pyinstaller = python -c "import PyInstaller" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "PyInstaller no encontrado. Instalando..." -ForegroundColor Yellow
    pip install pyinstaller
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error al instalar PyInstaller." -ForegroundColor Red
        exit 1
    }
    Write-Host "PyInstaller instalado correctamente." -ForegroundColor Green
} else {
    Write-Host "PyInstaller ya esta instalado." -ForegroundColor Green
}

Write-Host "Compilando UsbSwitch..." -ForegroundColor Cyan
python -m PyInstaller --onefile --noconsole --uac-admin --icon="usb.ico" --add-data "usb.ico;." --name "UsbSwitch" launcher.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error durante la compilacion." -ForegroundColor Red
    exit 1
}

Copy-Item -Path "disable.py" -Destination "dist\disable.py" -Force
Copy-Item -Path "enable.py"  -Destination "dist\enable.py"  -Force

Write-Host "Listo! ejecutable disponible en la carpeta dist" -ForegroundColor Green