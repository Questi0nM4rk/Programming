import cv2
import numpy as np

def encode(image_path, message_path, output_path):
    # Load the images
    image = cv2.imread(image_path)
    message = cv2.imread(message_path)

    # Ensure the images are the same size
    image = cv2.resize(image, (message.shape[1], message.shape[0]))

    # Convert the images to 8-bit unsigned integers
    image = np.uint8(image)
    message = np.uint8(message)

    # Shift the message image bits to the right
    message = message >> 7

    # Clear the least significant bit of the image
    image = image & 0b11111110

    # Combine the images
    encoded_image = image | message

    # Save the encoded image
    cv2.imwrite(output_path, encoded_image)


def decode(encoded_path, output_path):
    # Load the encoded image
    encoded_image = cv2.imread(encoded_path)

    # Extract the least significant bit of each pixel
    decoded_image = encoded_image & 0b00000001

    # Shift the bits to the left to make the message visible
    decoded_image = decoded_image << 7

    # Save the decoded image
    cv2.imwrite(output_path, decoded_image)
    

# Example usage:
name = 'pOO78Px2z1'
next = '9rH2U2cm6L'

text = "" + next

encode('image.png', 'message.png', f'{name}.png')
decode(f'{name}.png', 'decoded.png')