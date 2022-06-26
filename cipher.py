import random
import string
import sys
import os


class InputError(Exception):
    pass


def random_key(length):
    if length is None:
        raise InputError("The parameter 'length' is required")

    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits
    symbols = string.punctuation

    all = lower + upper + num + symbols

    key = ''
    for i in range(length):
        key += random.choice(all)

    return key


def repeat(string_to_repeat: str, length: int):
    if not isinstance(string_to_repeat, str):
        string_to_repeat = str(string_to_repeat)

    if not isinstance(length, int):
        raise InputError("The length parameter must be an integer")

    multiple = int(length / len(string_to_repeat) + 1)
    repeated_string = string_to_repeat * multiple
    return repeated_string[:length]


def algorithm(file_name, operation_type="cipher", key=None, verbose=False):
    if not file_name:
        raise InputError("The file_name parameter is required")

    if not file_name.endswith('.txt') or not os.path.exists(file_name):
        raise ValueError("The file_name parameter must be a .txt file name")

    # Read and extract the contents of the file.
    with open(file_name, "r") as f:
        file_content = f.read()

    # If the key is not passed, it is generated.
    if not key:
        key = random_key(len(file_content))

    if operation_type == "cipher":

        # If the key does not have the same length as the file contents, then we adjust it.
        if len(key) != len(file_content):
            key = repeat(key, len(file_content))

        # Pass key and file content to binary
        b_content = ''.join(format(ord(i), '08b') for i in file_content)
        b_key = ''.join(format(ord(i), '08b') for i in key)

        # Do the XOR operation
        cipher = int(b_content, 2) ^ int(b_key, 2)
        b_cipher = "{0:b}".format(cipher).zfill(len(b_key))

        # Convert all to decimal
        decimal_cipher = ' '.join(str(int(b_cipher[i:i + 8], 2)) for i in range(0, len(b_cipher), 8))

        # Write the final file
        with open("result_cipher.txt", "w") as f:
            f.write(decimal_cipher)

        if verbose:
            print("file_content: ", file_content, "len: ", len(key))
            print("key: ", key, "len: ", len(key))
            print("binary_content: ", b_content, "len: ", len(b_content))
            print("binary_key: ", b_key, "len: ", len(b_key))
            print("binary_cipher: ", b_cipher, "len: ", len(b_cipher))
            print("ascii_cipher: ", ascii(decimal_cipher), "len: ", len(decimal_cipher))

    elif operation_type == "decipher":
        # Decipher

        # Get file contents for decryption
        decimal_content = file_content.split(' ')
        b_cipher = ''.join(format(int(i), '08b') for i in decimal_content)

        # If the key does not have the same length as the file contents, then we adjust it.
        if len(key) != len(decimal_content):
            key = repeat(key, len(decimal_content))

        b_key = ''.join(format(ord(i), '08b') for i in key)

        # Do the XOR operation
        decipher = int(b_cipher, 2) ^ int(b_key, 2)
        b_decipher = "{0:b}".format(decipher).zfill(len(b_key))

        # Convert all to ASCII
        decipher_content = "".join(chr(int(b_decipher[i:i + 8], 2)) for i in range(0, len(b_decipher), 8))

        # Write the final file
        with open("result_decipher.txt", "w") as f:
            f.write(decipher_content)

        if verbose:
            print("binary_content: ", b_decipher, "len: ", len(b_decipher))
            print("binary_key: ", b_key, "len: ", len(b_key))
            print("binary_cipher_to_decipher: ", b_cipher, "len: ", len(b_cipher))
            print("ascii_decipher: ", decipher_content, "len: ", len(decipher_content))


def main():
    operation_type = "cipher"  # OR decipher
    verbose = False
    key = None

    if "--v" in sys.argv:
        verbose = bool(sys.argv.pop(sys.argv.index("--v")))

    tags = sys.argv[1::2]
    params = sys.argv[2::2]

    if "-f" in tags:
        pos = tags.index("-f")
        file_name = params[pos]
    else:
        raise InputError("-f <file name> parameter is required!")

    if "-p" in tags:
        pos = tags.index("-p")
        key = params[pos]

    if "-o" in tags:
        pos = tags.index("-o")
        operation_type = params[pos]

    algorithm(file_name, operation_type, key, verbose)


if __name__ == "__main__":
    main()
