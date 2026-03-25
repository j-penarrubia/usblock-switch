# 🛡️ USB AutoMount Switch

Herramienta gráfica desarrollada en Python para habilitar o deshabilitar rápidamente el montaje automático de dispositivos USB y la reproducción automática en sistemas Windows. 

Este proyecto está enfocado en el **Hardening y la Ciberseguridad**, diseñado para prevenir la modificación del hash global en dispositivos usb adquiridos al bloquear el reconocimiento automático de almacenamiento extraíble.

## ✨ Características

- **Interfaz Gráfica (GUI):** Panel de control intuitivo creado con Tkinter.
- **Auto-Elevación de Privilegios:** Solicita automáticamente permisos de Administrador (UAC) necesarios para modificar el registro y los servicios del sistema.
- **Bloqueo Profundo:** Modifica directivas de Registro (`HKLM` y `HKCU`), deshabilita la indexación de unidades extraíbles y detiene el servicio de almacenamiento (`StorSvc`).
- **Feedback en Tiempo Real:** Consola integrada en la interfaz que muestra el registro de operaciones y el estado actual del automontaje.

## 📋 Requisitos

Si solo deseas usar la herramienta, puedes descargar el ejecutable directamente desde la pestaña **[Releases](../../releases)** (No requiere tener Python instalado).

Para compilar la herramienta desde el código fuente necesitas:
- Windows 10 / Windows 11
- Python 3.x
- Permisos de Administrador

## 🚀 Instalación y Compilación

El proyecto incluye un script de automatización en PowerShell que verifica las dependencias, instala `PyInstaller` si es necesario y compila el ejecutable.

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/usblock.git
   cd usblock

2. Ejecuta el script de compilación desde PowerShell:
    .\build.ps1

3. El ejecutable compilado junto con los scripts necesarios aparecerá en la carpeta dist/.

## 📁 Estructura del Proyecto
launcher.py: Script principal que genera la interfaz gráfica y coordina la ejecución.

disable.py: Script que aplica las políticas de seguridad en el registro y servicios para bloquear USBs.

enable.py: Script que revierte los cambios y restaura el comportamiento por defecto de Windows.

build.ps1: Script de automatización para generar el .exe final.

usb.ico: Icono de la aplicación.

## ⚠️ Advertencia
Esta herramienta realiza modificaciones en el Registro de Windows y en los Servicios del Sistema. Se recomienda reiniciar el equipo después de aplicar o revertir los cambios para asegurar que el sistema operativo asimile correctamente las nuevas directivas de montaje. Úsalo bajo tu propia responsabilidad.