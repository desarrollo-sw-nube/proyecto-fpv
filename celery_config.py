

import logging
from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx
import os
from celery import Celery


def make_celery(app_name):
    celery_instance = Celery(app_name, broker='pyamqp://rabbitmq:5672/')
    return celery_instance


celery_instance = make_celery("video_tasks")

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


@celery_instance.task(name='process_video')
def process_video(filename):
    logging.info(f"Procesando el video {filename}")
    base_path = 'app/uploads'
    logo_path = 'app/assets/logo.mp4'

    input_path = os.path.join(base_path, filename)
    output_path = os.path.join(base_path, 'processed_' + filename)

    video = VideoFileClip(input_path)

    logo = VideoFileClip(logo_path).set_duration(2)

    if video.duration > 20:
        video = video.subclip(0, 20)

    video = video.resize(
        height=video.size[1], width=int(video.size[1] * 16 / 9))

    final_clip = concatenate_videoclips([logo, video, logo])

    final_clip.write_videofile(output_path, codec='libx264', fps=24)

    return f'Video processed and saved to uploads'
