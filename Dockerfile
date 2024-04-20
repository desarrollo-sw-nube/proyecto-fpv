# Usar una imagen oficial de Python como base
FROM python:3.9-slim


WORKDIR /worker

# Copiar los archivos del proyecto al contenedor
COPY . /worker

# Instalar las dependencias del proyecto
RUN pip install -r requirements.txt

# Exponer el puerto 8080
EXPOSE 8080

# CMD para montar el directorio NFS en el contenedor
RUN sudo apt install nfs-common
RUN mkdir /uploads
RUN echo "10.128.0.4:/home/jm2002_santosa/uploads /uploads nfs defaults 0 0" >> /etc/fstab
RUN sudo mount -a

# CMD para iniciar el worker de celery
CMD ["celery", "-A", "celery_config.celery_instance", "worker", "--loglevel=error"]