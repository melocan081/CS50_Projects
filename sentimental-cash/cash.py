from cs50 import get_float


def quarters(change):
    quarter_num = 0
    while change >= 25:
        quarter_num += 1
        change -= 25
    remaining = change
    return quarter_num, remaining


def dimes(change):
    dime_num = 0
    while change >= 10:
        dime_num += 1
        change -= 10
    remaining = change
    return dime_num, remaining


def nickels(change):
    nickel_num = 0
    while change >= 5:
        nickel_num += 1
        change -= 5
    remaining = change
    return nickel_num, remaining


def pennies(change):
    penny_num = 0
    while change >= 1:
        penny_num += 1
        change -= 1
    remaining = change
    return penny_num, remaining


change = get_float("Change: ")
while change < 0:
    change = get_float("Change: ")
change *= 100

quarter, remaining = quarters(change)

dime, remaining = dimes(remaining)

nickel, remaining = nickels(remaining)

penny, remaining = pennies(remaining)


total_coins = quarter + dime + nickel + penny

print(f"{str(total_coins)}\n")
