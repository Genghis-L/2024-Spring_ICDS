def adds_up(n):
    if n < 0:
        print("n should be nonnegative")
        return
    if n < 2:
        s = n
    else:
        s = n+adds_up(n-1)
    return s


if __name__ == "__main__":
    print(adds_up(100))
