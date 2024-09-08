
#!/bin/bash

# Variables
archivo_a_copiar="/home/abarrios/proyectos/mycsrl/db.sqlite3"  # Cambia esto por la ruta de tu archivo
directorio_respaldo="/home/abarrios/bck/bk_db.sqlite"    # Cambia esto por la ruta del directorio de respaldo
nombre_del_commit="Backup del archivo $(date +'%Y-%m-%d %H:%M:%S')"

# Copiar el archivo
cp "$archivo_a_copiar" "$directorio_respaldo"

# Navegar al directorio del repositorio Git (si no estás ya en él)
cd /home/abarrios/proyectos/mycsrl || exit  # Cambia esto por la ruta de tu repositorio

# Añadir los cambios al índice de Git
#git add "$directorio_respaldo/$(basename "$archivo_a_copiar")"
git add .

# Realizar el commit
git commit -m "$nombre_del_commit"

echo "Copia y commit realizados con éxito."
