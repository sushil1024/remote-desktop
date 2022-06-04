import random


# Generate random password
def genpass():
    lower = "abcdefghijklmnopqrstuvwxyz"
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numbers = "0123456789"

    string = lower + upper + numbers

    password = "".join(random.sample(string, 12))

    return password


if __name__ == '__main__':
    a = genpass()
    print(a)
