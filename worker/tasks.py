from google.cloud import storage, pubsub_v1
from moviepy.editor import VideoFileClip, concatenate_videoclips
from tempfile import NamedTemporaryFile
import os
from db import Task, TaskStatus
from init import db_session, topic_path, publisher
import json

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'secrets/gcp_keys.json'
storage_client = storage.Client()
bucket = storage_client.get_bucket('uniandes-fpv-videos')


def publish_message(file_path, file_name, task_id):
    message_data = {
        'file_path': file_path,
        'file_name': file_name,
        'task_id': task_id
    }
    future = publisher.publish(
        topic_path, json.dumps(message_data).encode('utf-8'))
    future.result()


def process_video(file_path, file_name, task_id):
    blob = bucket.blob(file_name)
    with NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video_file:
        blob.download_to_filename(temp_video_file.name)

    bash_script_path = '/app/resize.sh'
    logo_video_path = '/app/assets/logo.mp4'
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

    processed_blob = bucket.blob(logo_output_video_path)
    processed_blob.upload_from_filename(logo_output_video_path)

    db_session.query(Task).filter(Task.id == task_id).update(
        {Task.status: TaskStatus.PROCESSED}
    )
    db_session.commit()

    os.remove(output_video_path)
    os.remove(temp_video_file.name)
    os.remove(logo_output_video_path)

    return f"Video processed and uploaded as {processed_blob.public_url}."