import cv2
import numpy as np

def encode(image_path, message_path, output_path):
    # Load the images
    image = cv2.imread(image_path)
    message = cv2.imread(message_path, cv2.IMREAD_GRAYSCALE)

    # Ensure the images are the same size
    image = cv2.resize(image, (message.shape[1], message.shape[0]))

    # Make red channel even where message is white
    image[(message == 255) & (image[..., 2] % 2 != 0), 2] += 1

    # Make red channel odd where message is black
    image[(message == 0) & (image[..., 2] % 2 == 0), 2] += 1

    # Save the encoded image
    cv2.imwrite(output_path, image)

def decode(encoded_path, output_path):
    # Load the encoded image
    encoded = cv2.imread(encoded_path)

    # Create an empty array for the decoded message
    decoded = np.zeros((encoded.shape[0], encoded.shape[1]), dtype=np.uint8)

    # Set white where red channel is even
    decoded[encoded[..., 2] % 2 == 0] = 255

    # Save the decoded image
    cv2.imwrite(output_path, decoded)

# Example usage:
encode('image.png', 'message.png', 'encoded.png')
decode('image.png', 'decoded.png')