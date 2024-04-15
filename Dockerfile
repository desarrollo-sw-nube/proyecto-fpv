# Usar una imagen oficial de Python como base
FROM python:3.9-slim


WORKDIR /app

# Copiar los archivos del proyecto al contenedor
COPY . /app


# Instalar las dependencias del proyecto
RUN pip install -r requirements.txt

# Exponer el puerto 8080
EXPOSE 8080


# Comando para ejecutar la aplicación usando Gunicorn en el puerto 8080
CMD [ "gunicorn", "--bind", "0.0.0.0:8080", "app.app:app"]


