import csv
import sys


def main():
    # Ensure correct usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py database.csv sequence.txt")
        sys.exit(1)

    # Read database
    try:
        with open(sys.argv[1], "r") as db:
            database = list(csv.DictReader(db))
    except Exception as e:
        print(f"Error reading database file: {e}")
        sys.exit(1)

    # Read DNA sequence
    try:
        with open(sys.argv[2], "r") as seq:
            dna_sequence = seq.read().strip()
    except Exception as e:
        print(f"Error reading sequence file: {e}")
        sys.exit(1)

    # Extract STRs (the keys in the database beyond 'name')
    str_list = csv.DictReader(open(sys.argv[1])).fieldnames[1:]

    # Compute STR counts
    str_counts = {str_: longest_match(dna_sequence, str_) for str_ in str_list}

    # Check for matching profiles
    for person in database:
        # Compare STR counts against database values
        if all(int(person[str_]) == str_counts[str_] for str_ in str_list):
            print(person["name"])
            sys.exit(0)

    # If no match found
    print("No match")
    sys.exit(0)


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):
        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a substring (a subset of characters)
        while True:
            # Substring boundaries
            start = i + count * subsequence_length
            end = start + subsequence_length

            # Ensure we don't run out of bounds
            if end <= sequence_length and sequence[start:end] == subsequence:
                count += 1
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # Return longest run
    return longest_run


# Execute the main function
main()
