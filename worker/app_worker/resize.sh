#!/bin/bash

# Recibe los nombres de archivo de entrada y salida como argumentos
INPUT_VIDEO="$1"
OUTPUT_VIDEO="$2"

# Configura la resolución de salida en formato 4:3
WIDTH=1280
HEIGHT=720

# Comando para cambiar el aspect ratio
ffmpeg -i "$INPUT_VIDEO" -vf "scale=$WIDTH:$HEIGHT,setsar=1:1" -c:a copy "$OUTPUT_VIDEO"
