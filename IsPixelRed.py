from PIL import Image


def update_red_pixels(red_pixels, width, x, y):
    """
    Update the red pixels array if the pixel at (x, y) is red.
    :param red_pixels: Boolean array indicating red pixels.
    :param width: Width of the image.
    :param height: Height of the image.
    :param x: x-coordinate of the pixel.
    :param y: y-coordinate of the pixel.
    :param pixel: Tuple containing RGB values (R, G, B) of the pixel.
    """
    
    # Calculate the index of the pixel in the flattened array
    index = y * width + x

    # Set the corresponding element in the array to True
    red_pixels[index] = True

def is_red_pixel(pixel, threshold):
    """
    Check if a pixel is red based on RGB values.
    :param pixel: Tuple containing RGB values (R, G, B) of the pixel.
    :param threshold: Threshold value for the red color detection.
    :return: True if the pixel is red, False otherwise.
    """
    r, g, b = pixel

    # Check if the red component is significantly higher than the other components
    if r > threshold and r > g + threshold and r > b + threshold:
        return True
    else:
        return False


def calculate_false_negative(array1, array2):
    """
    Compare two boolean arrays and calculate the percentage of difference.
    :param array1: First boolean array.
    :param array2: Second boolean array.
    :return: Percentage of difference between the arrays.
    """
    if len(array1) != len(array2):
        raise ValueError("Arrays must have the same length.")

    total_elements = len(array1)
    false_negative = sum([1 for a, b in zip(array1, array2) if a and not b])

    false_negative_ratio = 1 - (false_negative / total_elements)
    return false_negative_ratio

def calculate_false_positive(array1, array2):
    """
    Compare two boolean arrays and calculate the percentage of difference.
    :param array1: First boolean array.
    :param array2: Second boolean array.
    :return: Percentage of difference between the arrays.
    """
    if len(array1) != len(array2):
        raise ValueError("Arrays must have the same length.")

    total_elements = len(array1)
    false_positive = sum([1 for a, b in zip(array1, array2) if b and not a])

    false_negative_ratio = 1 + (false_positive / total_elements)
    return false_negative_ratio

def update_threshold(threshold, false_negative, false_positive):
    return threshold * (false_positive) * ((false_negative + 1)/2)

def proccess_image_to_array(image_path, threshold):
    # Open the image
    image = Image.open(image_path)

    # Convert the image to RGB mode if it's not already
    image = image.convert("RGB")

    # Get the width and height of the image
    width, height = image.size

    # Initialize an empty boolean array
    red_pixels = [False] * (width * height)

    # Iterate over each pixel
    for y in range(height):
        for x in range(width):
            # Get the RGB values of the pixel at (x, y)
            pixel = image.getpixel((x, y))
            r, g, b = image.getpixel((x, y))

            # Check if the pixel is red
            if is_red_pixel(pixel, threshold):
                update_red_pixels(red_pixels, width, x, y)
    return red_pixels

def single_iteration_training(image_path, known_values, threshold):
    ai_values = proccess_image_to_array(image_path, threshold)

    false_negative = calculate_false_negative(known_values, ai_values)
    print(f"False negative ratio: {false_negative}")

    false_positive = calculate_false_positive(known_values, ai_values)
    print(f"False positive ratio: {false_positive}")

    threshold = update_threshold(threshold, false_negative, false_positive)
    
    return threshold, ai_values

def createImage(red_pixels, width, height):
    # Example array of pixel values (RGB tuples)
    white = (255, 255, 255)
    red = (255, 0, 0)

    # Create a new image with the given dimensions
    image = Image.new("RGB", (width, height))

    # Set the pixel values in the image
    for y in range(height):
        for x in range(width):
            if red_pixels[y * width + x]:
                pixel = red
            else:
                pixel = white
            image.putpixel((x, y), pixel)

    # Save the image to a file
    image.save("output_image.png")

image_path = 'apple.png'

# Create array with known values
known_values = [
    False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, 
    False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, 
    False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, 
    False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, 
    False, False, False, True,  True,  True,  True,  False, False, True,  True,  True,  True,  False, False, False, 
    False, False, True,  True,  False, True,  True,  False, True,  True,  False, False, True,  True,  False, False, 
    False, True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  False, 
    False, True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  False, 
    False, True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  False, 
    False, True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  False, 
    False, True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  False,
    False, False, True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  False, False,
    False, False, True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  False, False, 
    False, False, False, True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  False, False, False,
    False, False, False, True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  False, False, False,
    False, False, False, False, True,  True,  True,  True,  True,  True,  True,  True,  False, False, False, False,
]

threshold=1
print(f"Threshold: {threshold}")

iterations = 500

for i in range(0, iterations):
    threshold, red_pixels = single_iteration_training(image_path, known_values, threshold)
    print(f"Threshold {i + 1}: {threshold}")

createImage(red_pixels, 16, 16)