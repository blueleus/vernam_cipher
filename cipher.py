import random
import string


def random_key(length):
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits
    symbols = string.punctuation

    all = lower + upper + num + symbols

    key = ''
    for i in range(length):
        key += random.choice(all)

    return key


def main():
    file_content = None
    with open("el_principito_part1.txt", "r") as f:
        file_content = f.read()
    print("file_contnet: ", file_content)

    key = random_key(len(file_content))
    print("key: ", key)

    bcontent = ''.join(format(ord(i), '08b') for i in file_content)
    print("binary_content: ", bcontent, "len: ", len(bcontent))

    bkey = ''.join(format(ord(i), '08b') for i in key)
    print("binary_key: ", bkey, "len: ", len(bkey))

    cipher = int(bcontent, 2) ^ int(bkey, 2)
    bcipher = "{0:b}".format(cipher).zfill(len(bkey))
    print("binary_cipher: ", bcipher, "len: ", len(bcipher))

    decimal_cipher = ' '.join(str(int(bcipher[i:i + 8], 2)) for i in range(0, len(bcipher), 8))
    print("ascii_cipher: ", ascii(decimal_cipher), "len: ", len(decimal_cipher))

    with open("result_cipher.txt", "w") as f:
        f.write(decimal_cipher)

    # Decipher
    cipher_text = None
    with open("result_cipher.txt", "r") as f:
        cipher_text = f.read()

    bcipher = ''.join(format(int(i), '08b') for i in cipher_text.split(' '))
    print("binary_cipher_to_decipher: ", bcipher, "len: ", len(bcipher))

    decipher = int(bcipher, 2) ^ int(bkey, 2)
    bdecipher = "{0:b}".format(decipher).zfill(len(bkey))
    decipher_content = "".join(chr(int(bdecipher[i:i + 8], 2)) for i in range(0, len(bdecipher), 8))
    print("ascii_decipher: ", decipher_content, "len: ", len(decipher_content))


if __name__ == "__main__":
    main()
