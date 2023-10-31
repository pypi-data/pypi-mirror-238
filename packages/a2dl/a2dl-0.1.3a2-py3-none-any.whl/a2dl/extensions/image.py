""" Make images usable as icons """

IMAGES_WIDTH = "70"
IMAGES_HEIGHT = "70"

# Input and output as a PIL image
from rembg import remove
from PIL import Image

input_path = 'input.png'
output_path = 'output.png'

input = Image.open(input_path)
output = remove(input)
output.save(output_path)

raise NotImplementedError

# remove background
# https://github.com/danielgatis/rembg

# crop and resize

# save


