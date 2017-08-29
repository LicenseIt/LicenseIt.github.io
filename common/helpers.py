import random


def generate_password(length=10):
    ret = ''
    letters = [chr(c) for c in range(ord('A'), ord('Z') + 1)]
    small_letters = [chr(c) for c in range(ord('a'), ord('z') + 1)]
    letters.extend(small_letters)

    for num in range(length):
        ret += random.choice(letters)
    return ret
