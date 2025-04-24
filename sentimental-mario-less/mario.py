# Prompt the user for the height of the pyramid
while True:
    try:
        height = int(input("Height: "))
        if 1 <= height <= 8:  # Restrict height between 1 and 8, inclusive
            break
        else:
            print("Please enter a number between 1 and 8.")
    except ValueError:
        print("Please enter a valid number.")

# Build the half-pyramid
for i in range(1, height + 1):
    # Print spaces for alignment and then the hashes
    print(" " * (height - i) + "#" * i)
