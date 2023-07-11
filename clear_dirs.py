"""Quick script to clear output directories."""

import os
from glob import glob

# Create directories if they don't exist
#   Audio module has problems if the output/audio/ directory doesn't already exist

for path in (
    'output/',
    'output/renders',
    'output/audio',
    'output/video',
    'output/final'
):
    if not os.path.exists(path):
        os.makedirs(path)

# Clear the existing ones

files = glob('output/renders/*') +\
        glob('output/audio/*') +\
        glob('output/video/*') +\
        glob('output/final/*')

for f in files:
    os.remove(f)
