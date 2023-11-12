import cv2
import numpy as np


def text_to_bits(text):
    bits = bin(int.from_bytes(text.encode(), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def bits_to_text(bits):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()


def hide_text(image_path, text):
    # Load the image
    img = cv2.imread(image_path)

    # Convert text to binary
    binary = text_to_bits(text)

    for i in range(len(binary)):
        # Find the pixel to modify
        x = i // img.shape[1]
        y = i % img.shape[1]

        # Change the least significant bit of the pixel's blue color to be the bit from the text
        img[x, y, 0] = (img[x, y, 0] & 0xFE) | int(binary[i])

    # Save the modified image
    cv2.imwrite('hidden.png', img)


def extract_text(image_path, text_length):
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


def main():
    # Hide the text
    hide_text('image.png', 'Ns1DI4N5U9')

    # Extract the text
    print(extract_text('hidden.png', 13))


if __name__ == '__main__':
    main()
