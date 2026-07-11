from cs50 import get_int


def print_rows(bricks, spaces):
    print((" " * spaces) + ("#" * bricks))


while True:
    bricks = get_int("Bricks: ")
    if 1 <= bricks <= 8:
        break
spaces = bricks - 1

for i in range(bricks):
    print_rows(i + 1, spaces)
    spaces -= 1
