from app_worker import celery
from moviepy.editor import VideoFileClip, concatenate_videoclips
from tempfile import NamedTemporaryFile
from google.cloud import storage
import os
from app_worker.db import db, Task, TaskStatus


@celery.task(name='process_video')
def process_video(file_path, file_name, bucket_name, task_id):
    with NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video_file:
        # Suponiendo que file_path es una ruta accesible en el sistema de archivos
        with open(file_path, "rb") as f:
            temp_video_file.write(f.read())
        temp_video_file.close()

        logo_path = 'app/assets/logo.mp4'
        logo = VideoFileClip(logo_path).set_duration(2)
        video_clip = VideoFileClip(temp_video_file.name)

        if video_clip.duration > 20:
            video_clip = video_clip.subclip(0, 20)

        video_clip = concatenate_videoclips([logo, video_clip, logo])
        output_filename = "trimmed_" + file_name
        video_clip.write_videofile(output_filename, codec='libx264')

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        new_blob = bucket.blob(output_filename)
        new_blob.upload_from_filename(
            output_filename, content_type='video/mp4')
        
        db.session.query(Task).filter(Task.id == task_id).update(
            {Task.status: TaskStatus.PROCESSED}
        )

        os.remove(temp_video_file.name)
        os.remove(output_filename)

        return f"Video trimmed and uploaded as {output_filename}."
