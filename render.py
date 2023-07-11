"""
Rendering of Reddit visuals
"""

import pathlib

from PIL import Image
from html2image import Html2Image

from helpers import media, inject
import settings


BORDER_COLOR = (234, 51, 35, 255)

'''Render setup'''

hti = Html2Image(output_path='output/renders')

abs_path = pathlib.Path(__file__).parent.resolve()

css = inject(
    media('styles/RedditCSS.css'),
    abs_path=abs_path,
    max_post_width=settings.POST_WIDTH,
    max_comment_width=settings.COMMENT_WIDTH
)


'''Function definitions'''


def crop_border(path: str, save_as: str):
    """Crop an image across the red border."""

    img = Image.open(path)

    width, height = img.size

    # Top-left, bottom-left, bottom-right
    tl: tuple[int, int] = tuple()
    bl: tuple[int, int] = tuple()
    br: tuple[int, int] = tuple()

    # Find first red pixel

    for y in range(height):
        break_outer = False

        for x in range(width):

            # Found first red pixel
            if img.getpixel((x, y)) == BORDER_COLOR:
                tl = (x, y)

                break_outer = True
                break

        if break_outer:
            break

    # Descend vertically till we hit a white pixel

    for y in range(tl[1], height):

        # Found first red pixel
        if img.getpixel((tl[0], y)) != BORDER_COLOR:
            bl = (tl[0], y - 1)

            break

    # Travel horizontally till we hit a white pixel

    for x in range(bl[0], width):

        # Found first red pixel
        if img.getpixel((x, bl[1])) != BORDER_COLOR:
            br = (x, bl[1])

            break

    # Fix box values due to anti-aliasing
    tl = (tl[0] + 2, tl[1] + 2)
    br = (br[0] - 2, br[1] - 2)

    # Crop image using obtained coordinates and export
    img = img.crop(tl + br)

    # Save cropped image
    img.save(f'output/renders/{ save_as }.png', 'png')


def render_post(post):
    """Function to screenshot a post."""

    hti.screenshot(
        html_str=inject(media('templates/post.html'), **post),
        css_str=css,
        save_as=f'post.png'
    )

    crop_border(
        'output/renders/post.png',
        'post'
    )


def render_comments(comments):
    """Function to screenshot a comment."""

    # Screenshot comments

    hti.screenshot(
        html_str = [
            inject(media('templates/comment.html'), **c, abs_path=abs_path, avatar_index=(i % 4) + 1)
            for i, c in enumerate(comments)
        ],

        css_str=css,

        # H2IMG will automatically add numbers. Cool, huh?
        save_as=f'comment.png'
    )

    # Crop borders

    for ci in range(len(comments)):
        crop_border(
            f'output/renders/comment_{ ci }.png',
            f'comment_{ ci }'
        )
