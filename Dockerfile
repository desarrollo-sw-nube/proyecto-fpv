# Usar una imagen oficial de Python como base
FROM python:3.9-slim


WORKDIR /app

# Copiar los archivos del proyecto al contenedor
COPY . /app


# Instalar las dependencias del proyecto
RUN pip install -r requirements.txt

# Exponer el puerto 8080
EXPOSE 8080

# CMD para montar el directorio NFS en el contenedor
RUN mkdir /uploads
RUN echo "servidor_nfs:/ruta/en/el/servidor /uploads nfs defaults 0 0" >> /etc/fstab

# CMD para iniciar el worker de celery
CMD ["celery", "-A", "celery_config.celery_instance", "worker", "--loglevel=error"]


