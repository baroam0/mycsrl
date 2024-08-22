#!/bin/bash
# Ruta local del archivo a respaldar
#ARCHIVO_LOCAL="/home/abarrios/tmp/ups.txt"
# Ruta remota en OneDrive (debe coincidir con el nombre que configuraste en rclone)
#RUTA_ONEDRIVE="remote:onedrive"
# Realiza la copia de seguridad
#rclone copy "$ARCHIVO_LOCAL" "$RUTA_ONEDRIVE"

rclone copy "/home/abarrios/tmp/ups.txt" "onedrive:"

