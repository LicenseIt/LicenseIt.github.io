import random


def generate_password(length=10):
    ret = ''
    letters = [chr(c) for c in range(ord('A'), ord('z') + 1)]
    for num in range(length):
        ret += random.choice(letters)
    return ret
