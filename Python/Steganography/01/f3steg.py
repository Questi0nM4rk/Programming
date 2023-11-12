import cv2
import numpy as np

def text_to_bits(text):
    return ''.join(format(ord(char), '08b') for char in text)

def bits_to_text(bits):
    return ''.join(chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8))

def f3_encode(image_path, secret_message):
    # Load the image
    img = cv2.imread(image_path)

    # Convert the secret message to bits
    bits = text_to_bits(secret_message)

    # Embed the bits into the image
    bit_index = 0
    for i in range(img.size):
        # Find the pixel
        x = i // img.shape[1]
        y = i % img.shape[1]

        # Embed the bit into the pixel if it's different from the LSB
        if str(img[x, y, 0] & 0x1) != bits[bit_index]:
            img[x, y, 0] ^= 0x1

        bit_index += 1
        if bit_index == len(bits):
            break

    # Save the stego image
    cv2.imwrite('stego.png', img)

def f3_decode(image_path, text_length):
    # Load the image
    img = cv2.imread(image_path)

    # Extract the bits
    bits = ""
    for i in range(text_length * 8):
        # Find the pixel
        x = i // img.shape[1]
        y = i % img.shape[1]

        # Extract the least significant bit of the pixel's blue color
        bits += str(img[x, y, 0] & 0x1)

    # Convert the bits to text
    return bits_to_text(bits)

# Example usage
f3_encode('image.png', 'iHC438uwRv')
decoded_message = f3_decode('stego.png', 10)
print(decoded_message)