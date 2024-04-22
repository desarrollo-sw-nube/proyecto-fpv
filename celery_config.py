

import logging
from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx
import os
from celery import Celery
from google.cloud import storage
from tempfile import NamedTemporaryFile


def make_celery(app_name):
    celery_instance = Celery(app_name, broker='pyamqp://rabbitmq:5672/')
    return celery_instance


celery_instance = make_celery("video_tasks")

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


@celery_instance.task(name='process_video')
def process_video(file_stream, file_name, bucket_name):
    with NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video_file:
        temp_video_file.write(file_stream.read())
        temp_video_file.close()
        logo_path = 'app/assets/logo.mp4'
        logo = VideoFileClip(logo_path).set_duration(2)
        # Cargar el video con MoviePy
        video_clip = VideoFileClip(temp_video_file.name)

        # Cortar el video a 20 segundos si es necesario
        if video_clip.duration > 1:
            # Corta el video desde el inicio hasta los 20 segundos
            video_clip = video_clip.subclip(0, 1)
        # video_clip = video_clip.resize(
        #     height=video_clip.size[1], width=int(video_clip.size[1] * 16 / 9))

        video_clip = concatenate_videoclips([logo, video_clip, logo])
        # Guardar el video modificado
        output_filename = "trimmed_" + file_name
        video_clip.write_videofile(output_filename, codec='libx264')

    # Configurar el cliente de GCP Storage y subir el video recortado
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    new_blob = bucket.blob(output_filename)
    new_blob.upload_from_filename(output_filename, content_type='video/mp4')

    # Limpiar: eliminar los archivos temporales locales
    os.remove(temp_video_file.name)
    os.remove(output_filename)

    print(f"Video trimmed and uploaded as {output_filename}.")
# @celery_instance.task(name='process_video')
# def process_video(filename):
#     logging.info(f"Procesando el video {filename}")

#     bucket_name = 'fpv_bucket'
#     base_path = 'app/videos/'
#     logo_path = 'app/assets/logo.mp4'
#     input_path = os.path.join(base_path, filename)
#     output_path = os.path.join(base_path, 'processed_' + filename)

#     client = storage.Client()
#     bucket = client.bucket(bucket_name)
#     blob = bucket.blob(filename)

#     if not os.path.exists(base_path):
#         os.makedirs(base_path)

#     blob.download_to_filename(input_path)
#     logging.info(f"Descargado {filename} a {input_path}")

#     video = VideoFileClip(input_path)
#     logo = VideoFileClip(logo_path).set_duration(2)

#     if video.duration > 20:
#         video = video.subclip(0, 20)

#     # video = video.resize(
#     #     height=video.size[1], width=int(video.size[1] * 16 / 9))

#     final_clip = concatenate_videoclips([logo, video, logo])

#     final_clip.write_videofile(output_path, codec='libx264', fps=24)
#     logging.info(f"Video procesado y guardado en {output_path}")

#     return f'Video processed and saved to uploads'
