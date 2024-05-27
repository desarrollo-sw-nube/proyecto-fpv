import logging
import ffmpeg
from google.cloud import storage
from moviepy.editor import VideoFileClip, concatenate_videoclips
from db import Task, TaskStatus
from init import db_session
import tempfile
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'secrets/gcp_keys.json'
storage_client = storage.Client()
bucket = storage_client.get_bucket('uniandes-fpv-videos')

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def process_video(file_path, file_name, task_id):
    try:
        logger.info('Processing video %s', file_name)
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_video_path = os.path.join(temp_dir, 'input_video.mp4')
            output_video_path = os.path.join(
                temp_dir, f'processed_{file_name}')
            logo_output_video_path = os.path.join(
                temp_dir, f'logo_{file_name}')

            blob = bucket.blob(file_name)
            blob.download_to_filename(temp_video_path)

            logger.info('Resizing video')
            ffmpeg.input(temp_video_path).filter(
                'scale', 1280, 720).output(output_video_path).run()
            logger.info('Video resized')

            logo_video_path = 'assets/logo.mp4'
            logo = VideoFileClip(logo_video_path).set_duration(2)
            video_clip = VideoFileClip(output_video_path)

            if video_clip.duration > 20:
                video_clip = video_clip.subclip(0, 20)

            final_clip = concatenate_videoclips([logo, video_clip, logo])
            logger.info('Video with logo created')

            final_clip.write_videofile(logo_output_video_path, codec='libx264')
            logger.info('Final video with logo written')

            final_blob = bucket.blob(f'logo_{file_name}')
            final_blob.upload_from_filename(logo_output_video_path)
            logger.info('Final video with logo uploaded')

            db_session.query(Task).filter(Task.id == task_id).update(
                {Task.status: TaskStatus.PROCESSED}
            )
            db_session.commit()
            logger.info('Task updated in database')

            return f"Video processed and uploaded as {final_blob.public_url}"

    except Exception as e:
        logger.error(f"Error processing video {file_name}: {e}")
        print(f"Error processing video {file_name}: {e}")
