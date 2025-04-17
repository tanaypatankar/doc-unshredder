from PIL import Image
import random

def shred_image(image_path, strip_size=9, vertical=True):
    """
    Shreds an image into vertical or horizontal strips of a given size, shuffles them, and returns the shuffled list.

    :param image_path: Full path to the image file (string). 
                        The image will be opened from this path.
    :param strip_size: Integer size of each strip in pixels. 
                        The strip size will be applied to the width for vertical strips 
                        or to the height for horizontal strips. Default is 9.
    :param vertical: Boolean flag indicating the direction of the strips. 
                     If True, the image will be shredded into vertical strips. 
                     If False, the image will be shredded into horizontal strips. Default is True.
    :return: List of PIL.Image strips (shuffled if random.shuffle() is enabled). 
             Each element in the list is a PIL.Image object representing a strip.
    
    """
    
    # Open the image using the provided image path
    image = Image.open(image_path)
    width, height = image.size

    strips = []

    # Create vertical strips (split the image into vertical sections)
    if vertical:
        for i in range(width // strip_size):
            left = i * strip_size
            right = left + strip_size
            strip = image.crop((left, 0, right, height))  # Vertical strip
            strips.append(strip)
    else:
    # Create horizontal strips (split the image into horizontal sections)
        for i in range(height // strip_size):
            top = i * strip_size
            bottom = top + strip_size
            strip = image.crop((0, top, width, bottom))  # Horizontal strip
            strips.append(strip)

    # Shuffle the strips to randomize their order
    random.shuffle(strips)

    return strips