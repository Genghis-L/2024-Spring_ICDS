def transformer(value, format): # Transform a format number to decimal number
    result = 0
    power = 0
    while value:
        value, residual = divmod(value, 10)
        result += residual * format ** power
        power += 1
    return result

a = transformer(2023, 4)
print(a)

print(bin(a))
