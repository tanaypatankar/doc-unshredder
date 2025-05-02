from PIL import Image
import random

def shred_image(image_path, strip_size=9, vertical=True, shuffle=True):
    """
    Shreds an image into vertical or horizontal strips of a given size, shuffles them, and returns the shuffled list.

    :param image_path: Path to the image file.
    :param strip_size: Width (if vertical) or height (if horizontal) of each strip in pixels.
    :param vertical: If False, the image is rotated to apply vertical shredding logic.
    :return: List of shuffled PIL.Image strips.
    """
    image = Image.open(image_path)
    
    if not vertical:
        # Rotate 90 degrees to treat horizontal strips as vertical
        image = image.rotate(90, expand=True)

    width, height = image.size
    strips = []

    for i in range(width // strip_size):
        left = i * strip_size
        right = left + strip_size
        strip = image.crop((left, 0, right, height))
        strips.append(strip)

    if shuffle:
        # Shuffle the strips
        random.seed(50)
        random.shuffle(strips)

    return strips
