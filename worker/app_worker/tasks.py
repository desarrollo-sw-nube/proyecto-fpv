from app_worker import celery
from moviepy.editor import VideoFileClip, concatenate_videoclips
from tempfile import NamedTemporaryFile
import os
from app_worker.db import db, Task, TaskStatus
from api import app


@celery.task(name='process_video')
def process_video(file_path, file_name, task_id):
    with app.app_context():
        with NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video_file:
            with open(file_path, "rb") as f:
                temp_video_file.write(f.read())
            temp_video_file.close()

            logo_path = 'app_worker/assets/logo.mp4'
            logo = VideoFileClip(logo_path).set_duration(2)
            video_clip = VideoFileClip(temp_video_file.name)

            if video_clip.duration > 20:
                video_clip = video_clip.subclip(0, 20)

            video_clip = concatenate_videoclips([logo, video_clip, logo])
            output_filename = "trimmed_" + file_name
            if not output_filename.endswith('.mp4'):
                output_filename += '.mp4'
            full_output_path = os.path.join('uploads', output_filename)
            video_clip.write_videofile(full_output_path, codec='libx264')
            print(task_id)
            db.session.query(Task).filter(Task.id == task_id).update(
                {Task.status: TaskStatus.PROCESSED}
            )
            db.session.commit()
            os.remove(temp_video_file.name)

            return f"Video trimmed and uploaded as {full_output_path}."
