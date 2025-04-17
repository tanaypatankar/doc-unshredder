from PIL import Image

def shred_image(image_path):
    """
    Shreds an image into 9 even vertical strips and returns a list of image strips.
    
    :param image_path: Path to the input image.
    :return: List of 9 image strips.
    """
    image = Image.open(image_path)
    width, height = image.size
    strip_width = width // 9  # Calculate the width of each strip

    strips = []
    for i in range(9):
        left = i * strip_width
        right = left + strip_width
        strip = image.crop((left, 0, right, height))  # Crop the strip
        strips.append(strip)

    return strips
