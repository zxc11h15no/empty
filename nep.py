def sep(num):
    num = int(num)
    count = 0
    value = abs(num)

    while value != 0:
        count += int(value % 10 == 0)
        value //= 10

    return count

print(sep(22009))