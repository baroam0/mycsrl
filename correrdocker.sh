
# Build de la imagen
podman build -t django32-app .

podman run -it --rm -p 8000:8000 -v $(pwd):/app django32-app
