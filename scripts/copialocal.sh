#!/bin/bash

# Variables
FECHA_Y_HORA=$(date "+%d-%m-%y_%H-%M-%S")
NOMBRE_ARCHIVO="respaldo_$FECHA_Y_HORA.tgz"
CARPETA_RESPALDAR="/ruta/a/tu/carpeta"
CARPETA_DESTINO="./respaldos"
RCLONE_REMOTE="onedrive:backups"
WINDOWS_USER="usuario"
WINDOWS_IP="192.168.1.100"
WINDOWS_DESTINO="C:/respaldos"

# Crear el directorio de respaldo si no existe
mkdir -p "$CARPETA_DESTINO"

# Comprimir la carpeta
tar -czvf "$CARPETA_DESTINO/$NOMBRE_ARCHIVO" "$CARPETA_RESPALDAR"

# Subir a la nube usando rclone
# rclone copy "$CARPETA_DESTINO/$NOMBRE_ARCHIVO" "$RCLONE_REMOTE"

# Copiar a la PC con Windows usando SCP
scp "$CARPETA_DESTINO/$NOMBRE_ARCHIVO" "$WINDOWS_USER@$WINDOWS_IP:$WINDOWS_DESTINO"
