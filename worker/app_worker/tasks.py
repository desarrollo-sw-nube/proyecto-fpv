from app_worker import celery
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video.fx.resize import resize
from tempfile import NamedTemporaryFile
import os
from app_worker.db import db, Task, TaskStatus
from api import app
import subprocess


@celery.task(name='process_video')
def process_video(file_path, file_name, task_id):
    with app.app_context():
        with NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video_file:
            with open(file_path, "rb") as f:
                temp_video_file.write(f.read())
            temp_video_file.close()

            bash_script_path = '/app/app_worker/resize.sh'
            logo_video_path = '/app/app_worker/assets/logo.mp4'
            logo = VideoFileClip(logo_video_path).set_duration(2)

            output_video_path = os.path.join(
                'uploads', 'processed_' + file_name)
            logo_output_video_path = os.path.join(
                'uploads', 'logo_' + file_name)
            if not logo_output_video_path.endswith('.mp4'):
                logo_output_video_path += '.mp4'
            if not output_video_path.endswith('.mp4'):
                output_video_path += '.mp4'
            subprocess.call(
                [bash_script_path, temp_video_file.name, output_video_path])

            video_clip = VideoFileClip(output_video_path)
            if video_clip.duration > 20:
                video_clip = video_clip.subclip(0, 20)
            video_clip = concatenate_videoclips([logo, video_clip, logo])
            video_clip.write_videofile(logo_output_video_path, codec='libx264')
            db.session.query(Task).filter(Task.id == task_id).update(
                {Task.status: TaskStatus.PROCESSED}
            )
            db.session.commit()
            os.remove(output_video_path)
            os.remove(temp_video_file.name)

            return f"Video processed and uploaded as {output_video_path}."
