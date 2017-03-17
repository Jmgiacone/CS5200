def main():
    square = generate_magic_square(3)

    print_magic_square(square)

    if not is_magic_square(square):
        print("Error!")


def print_magic_square(square):
    n = len(square)
    padding = len(str(n ** 2 - 1))

    for i in range(n):
        for j in range(n):
            print(str(square[i][j]).zfill(padding), end=" ")
        print()


def is_magic_square(square):
    n = len(square)

    # There are no magic squares of n <= 2
    if n <= 2:
        return False

    # The number that every row, column, and diagonal needs to add up to
    magic_number = (n * (n ** 2 + 1)) // 2

    # Set up sums
    rows = [0] * n
    columns = [0] * n
    left_diag = 0
    right_diag = 0

    # Calculate all 3 sums in one double loop
    for i in range(n):
        for j in range(n):
            rows[i] += square[i][j]
            columns[i] += square[j][i]

            if i == j:
                left_diag += square[i][i]
                right_diag += square[i][n - 1 - i]

        # Check the row and column that we just computed
        if not (rows[i] == columns[i] == magic_number):
            return False

    return left_diag == right_diag == magic_number


def generate_magic_square(n):
    # There are no magic squares of n <= 2
    if n <= 2:
        return None

    # Create a 2d array of size n x n
    magic_square = [0] * n

    for i in range(n):
        magic_square[i] = [0] * n

    # Initialize the counter
    counter = 1

    if n % 2 == 1:
        # 1: n is odd
        row, column = 0, n // 2

        for i in range(1, n ** 2 + 1, 1):
            magic_square[row][column] = i

            # Up 1, over 1
            r = (row - 1) % n
            c = (column + 1) % n

            # If this space is occupied
            if magic_square[r][c] != 0:
                r = (row + 1) % n
                c = column

            # Copy over r, c values
            row, column = r, c

        return magic_square

    elif n % 2 == 0 and n % 4 != 0:
        # 2: n is singly even (divisible by 2 but not by 4 -> 4n + 2)
        pass
    else:
        # n is doubly even (divisible by 2 and 4 -> 4n)
        pass

if __name__ == "__main__":
    main()
