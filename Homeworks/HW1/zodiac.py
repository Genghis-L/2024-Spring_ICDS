# get user input
your_year = input("Enter a year: ")

# you code needs to do the following things:
# 1. check if it is a integer; if not, ask the user to re input
# 2. check if it is non negative; if not, ask the user to re input
# 3. print the user's animal of the year on the screen

# check if it is a integer
while not your_year.isdigit():
    your_year = input("Error: You need to enter a integer! \nEnter a year: ")

# check if it is non negative
while float(your_year) < 0:
    your_year = input(
        "Error: You need to enter a non negtive integer! \nEnter a year: ")


d = {8: "Dragon", 9: "Snake", 10: "Horse", 11: "Sheep", 0: "Monkey",
     1: "Rooster", 2: "Dog", 3: "Pig", 4: "Rat", 5: "Ox", 6: "Tiger", 7: "Hare"}

answer = d[int(your_year) % 12]
print(f"{your_year} is the year of {answer}. ")
