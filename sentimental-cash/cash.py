# taking user input
while True:
    try:
        change = float(input("Change: "))
        if change >= 0:
            break
    except ValueError:
        pass
    print("Invalid input.")

# converting dollars to cents
cents = round(change * 100)

# calculating the minimum number of coins
coins = 0
for denomination in [25, 10, 5, 1]:
    coins += cents // denomination
    cents %= denomination

# Output the result
print(coins)
