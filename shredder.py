from PIL import Image
import random

def shred_image_vertically(image_path, strip_width=9):
    """
    Shreds an image into vertical strips of a given width, shuffles them, and returns the shuffled list.

    :param image_path: Path to the input image.
    :param strip_width: Width of each strip.
    :return: List of shuffled image strips.
    """
    image = Image.open(image_path)
    width, height = image.size

    strips = []
    for i in range(width // strip_width):
        left = i * strip_width
        right = left + strip_width
        strip = image.crop((left, 0, right, height))  # Crop the strip
        strips.append(strip)

    random.shuffle(strips)  # Shuffle the strips randomly

    return strips
