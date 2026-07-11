import csv
from sys import argv, exit


def main():

    # TODO: Check for command-line usage
    if len(argv) != 3:
        print("3 CLAs please.")
        exit(1)

    file_no_1 = argv[1]
    file_no_2 = argv[2]

    # TODO: Read database file into a variable
    database = []

    with open(file_no_1) as file:
        reader = csv.DictReader(file)
        for data in reader:
            database.append(data)

    # TODO: Read DNA sequence file into a variable
    sequence = []
    with open(file_no_2) as file2:
        sequence = file2.read()


    # TODO: Find longest match of each STR in DNA sequence
    strs = []
    for st in reader.fieldnames:
        next(reader.fieldnames)
        strs.append(st)
    longest_ones = []
    for s in strs:
        longest = str(longest_match(sequence, s))
        longest_ones.append(longest)

    # TODO: Check database for matching profiles
    str_count = len(reader.fieldnames[1:])

    for variables in database:
        counter = 0
        for strrr in variables.keys():
            if strrr != "name":
                if variables[strrr] == longest_ones[counter]:
                    counter += 1
                    if counter == str_count:
                        print(f'{variables["name"]}')
                        exit(0)


    print("No match.")

    return


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

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
