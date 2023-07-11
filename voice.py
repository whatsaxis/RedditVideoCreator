"""
Generating TTS of the text
"""

from gtts import gTTS

from pydub import AudioSegment
from pydub.effects import speedup

import settings


def generate_post_tts(post):
    """Function to generate the audio of a post."""

    tts = gTTS(text=post['title'], lang='en', tld='com.au')
    tts.save('output/audio/post_audio.mp3')


def generate_comment_tts(comment, index):
    """Function to generate the audio of a comment."""

    # Get comment contents
    body = comment['body']

    # Generate TTS
    tts = gTTS(text=body, lang='en', tld='com.au')
    tts.save(f'output/audio/comment_{ index }_audio.mp3')


def create_audio_files(post, comments):
    """Function to create final audio file."""

    # Generate raw TTS

    generate_post_tts(post)

    for i, comment in enumerate(comments):
        generate_comment_tts(comment, index=i)

    # Speed up audio

    post_audio_file = speedup(
        AudioSegment.from_mp3('output/audio/post_audio.mp3'),
        settings.AUDIO_SPEEDUP
    )

    comment_audio_files = tuple(

        speedup(
            AudioSegment.from_mp3(f'output/audio/comment_{ i }_audio.mp3'),
            settings.AUDIO_SPEEDUP
        )

        for i in range(settings.NUM_COMMENTS)

    )

    return (
        post_audio_file,
        comment_audio_files
    )


def create_audio(post_audio, comment_audios):
    """Create final audio file."""

    audio_out = AudioSegment.empty()

    audio_out += post_audio
    audio_out += AudioSegment.silent(settings.TRANSITION_DURATION * 1000)

    for i, a in enumerate(comment_audios):

        # Add a 1000ms offset... for some reason?
        audio_out += AudioSegment.silent(settings.TRANSITION_DURATION * 1000)

        audio_out += a

        # No transition on the last one
        if i != len(comment_audios):
            audio_out += AudioSegment.silent(settings.TRANSITION_DURATION * 1000)

    return audio_out


def compute_audio_durations(post_audio, comment_audios):
    """Function to compute the durations of the audio clips."""

    return (

        # Post
        post_audio.duration_seconds,

        # Comments
        tuple(
            f.duration_seconds
            for f in comment_audios
        )

    )
