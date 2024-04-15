# import os
# from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx
# from celery_config import celery as celery_app
# import logging

# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s - %(levelname)s - %(message)s')


# @celery_app.task(bind=True)
# def process_video(filename):
#     logging.info(f"Procesando el video {filename}")
#     input_path = os.path.join('./app/uploads', filename)
#     output_path = os.path.join('./app/uploads', filename)

#     try:
#         clip = VideoFileClip(input_path)
#         clip = clip.resize((clip.size[0], int(clip.size[0] * 9 / 16)))
#         clip = clip.subclip(0, 16).fx(vfx.fadein, 0.5).fx(vfx.fadeout, 0.5)

#         logo = VideoFileClip('./app/assets/logo.mp4').subclip(0,
#                                                               2).fx(vfx.fadein, 0.5).fx(vfx.fadeout, 0.5)
#         clip = concatenate_videoclips([logo, clip, logo])

#         clip.write_videofile(output_path)
#         logging.info(f"Video procesado: {filename}")
#     except Exception as e:
#         print(f"Error procesando el video {filename}: {e}")
#     clip.close()