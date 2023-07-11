"""
Video Creation Module
"""

import math

import cv2

import settings


video = cv2.VideoCapture(settings.BG)
current_frame = 0


def add_to_video(video_writer, image, length):
    """Function to write to the video with a transition."""

    global current_frame

    # Get dimensions of a frame of video

    video.set(cv2.CAP_PROP_POS_FRAMES, 0)
    _, frame = video.read()

    # Overlay image over the background frame

    img_x, img_y = image.shape[1], image.shape[0]
    bg_x, bg_y = frame.shape[1], frame.shape[0]

    # Compute centering offset

    offset_x, offset_y = (bg_x - img_x) // 2, (bg_y - img_y) // 2

    for _ in range(settings.VIDEO_FPS * math.ceil(length)):

        # Get background frame
        video.set(cv2.CAP_PROP_POS_FRAMES, current_frame - 1)
        _, frame = video.read()

        # Overlay image
        frame[
            offset_y:offset_y + img_y,
            offset_x:offset_x + img_x
        ] = image

        # Write to video
        video_writer.write(frame)
        current_frame += 1

    # Add transition
    for _ in range(settings.VIDEO_FPS * settings.TRANSITION_DURATION):

        # Get background frame
        video.set(cv2.CAP_PROP_POS_FRAMES, current_frame - 1)
        res, frame = video.read()

        video_writer.write(frame)
        current_frame += 1
