import cv2
import moviepy.editor as mpe

import settings

from fetch import get_json, get_post, get_comments

from render import render_post, render_comments
from voice import create_audio, create_audio_files, compute_audio_durations
from video import add_to_video


# TODO Functions for accessing renders and output folders.

"""
Fetching data
"""

data = get_json(settings.POST_ID)

post = get_post(data)
comments = get_comments(data)[:settings.NUM_COMMENTS]

print('[INFO] Fetched data!')


"""
Rendering post and comments
"""

render_post(post)
render_comments(comments)

print('[INFO] Finished rendering post and comments!')

"""
Speech Generation
"""

post_audio, comment_audios = create_audio_files(post, comments)
audio_final = create_audio(post_audio, comment_audios)

audio_final.export('output/audio/audio_final.mp3', format='mp3')

print('[INFO] Finished exporting audio!')

# Export final audio

post_duration, comment_durations = compute_audio_durations(post_audio, comment_audios)

"""YouTube Short Mode"""

# Calculate number of comments to be played if in YouTube mode.
# YouTube shorts must be ≤ 60 seconds

# NOTE: TRANSITION_DURATION of the post is accounted for as we do not
# exclude it for the last comment in the loop, so it can be considered
# as the one from the post.

if settings.YOUTUBE_SHORTS:

    num_comments = 0
    remaining_time = 60 - post_duration

    while remaining_time > 0:

        duration = comment_durations[num_comments]

        if remaining_time - duration - settings.TRANSITION_DURATION < 0:
            break

        remaining_time -= duration + settings.TRANSITION_DURATION
        num_comments += 1

    # Slice comment audio

    comments = comments[:num_comments]
    comment_audio_files = comment_audios[:num_comments]

"""
Video Creation
"""

vw = cv2.VideoWriter(
    'output/video/video.avi',
    cv2.VideoWriter.fourcc(*'DIVX'),
    settings.VIDEO_FPS,
    settings.VIDEO_RES
)


# Add post

add_to_video(
    video_writer=vw,
    image=cv2.imread('output/renders/post.png'),
    length=post_duration
)


# Add comments

for ci in range(len(comments)):
    img = cv2.imread(f'output/renders/comment_{ ci }.png')

    add_to_video(
        video_writer=vw,
        image=img,
        length=comment_durations[ci]
    )


# Export video
vw.release()

print('[INFO] Finished exporting video!')

"""
Overlay Audio
"""

video = mpe.VideoFileClip('output/video/video.avi')
audio = mpe.AudioFileClip('output/audio/audio_final.mp3')

final = video.set_audio(audio)

final.write_videofile('output/final/video_final.mp4')

print('[INFO] Finished exporting video + audio overlay!')
