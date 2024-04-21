#!/bin/bash

# Definir el puerto predeterminado si PORT no está establecido
PORT=${PORT:-5000}

# Ejecutar Flask
exec python -m flask run --host=0.0.0.0 --port=$PORT
