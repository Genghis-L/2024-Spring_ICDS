import threading


def change_num(num):
    while True:
        num[0] = 0


def process():
    process = threading.Thread(target=lambda: change_num(num))
    process.daemon = True
    process.start()


num = [0]
process()
while True:  ##Question: will this while loop stop?
    num[0] += 1
    print(num)

    if num[0] == 0:
        break
