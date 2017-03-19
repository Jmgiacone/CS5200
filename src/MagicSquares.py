from copy import deepcopy


def main():
    for i in range(3, 51):
        print("Magic square for n={}".format(i))
        square = generate_magic_square(i)

        if square is not None:
            print_magic_square(square)

            if not is_magic_square(square):
                print("Error!")
                break
            else:
                print("This is a magic square!")
        else:
            print("Not implemented")
        print()


def print_magic_square(square):
    n = len(square)
    padding = len(str(n ** 2))

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
        # 2: n is singly even (divisible by 2 but not by 4 -> 4k + 2)

        # Generate the k value
        k = (n - 2) // 4

        # Left-hand column width
        a_d_column_width = k

        # Right-hand column width
        c_b_column_width = k - 1

        # Split the square into 4 parts of n/2 -> a, b, c ,d
        half_size = n // 2
        a_square = generate_magic_square(half_size)
        b_square = deepcopy(a_square)
        c_square = deepcopy(b_square)
        d_square = deepcopy(c_square)

        # Edit the values of squares b, c, and d. Make it look as if these magic squares were started at different
        # numbers than they actually were: n^2/4 + 1, n^2/2 + 1, and 3n^2/2 + 1 specifically
        b_number = half_size ** 2
        c_number = 2 * b_number
        d_number = 3 * b_number
        for i in range(half_size):
            for j in range(half_size):
                b_square[i][j] += b_number
                c_square[i][j] += c_number
                d_square[i][j] += d_number

        # The halfway index is where we shift everything over one column
        halfway_index = half_size // 2

        # Generate a rectangle of n/2 x k and push the middle over by one in both a and d
        for i in range(half_size):
            for j in range(a_d_column_width):
                offset = 0
                if i == halfway_index:
                    # Push everything over by 1 column
                    offset = 1

                # Swap these values between a and d
                temp = a_square[i][j + offset]
                a_square[i][j + offset] = d_square[i][j + offset]
                d_square[i][j + offset] = temp

        # Generate a rectangle of n/2 x k-1 and swap them between c and b
        for i in range(half_size):
            for j in range(c_b_column_width):
                # Swap
                temp = c_square[i][half_size - 1 - j]
                c_square[i][half_size - 1 - j] = b_square[i][half_size - 1 - j]
                b_square[i][half_size - 1 - j] = temp

        # Conquer the sub-problems
        for i in range(half_size):
            for j in range(half_size):
                # Directly copy the upper-left quarter
                magic_square[i][j] = a_square[i][j]

                # Copy the upper-right quarter with a column shift
                magic_square[i][j + half_size] = c_square[i][j]

                # Copy the bottom-left quarter with a row shift
                magic_square[i + half_size][j] = d_square[i][j]

                # Copy the bottom-right quarter with a row and column shift
                magic_square[i + half_size][j + half_size] = b_square[i][j]

        return magic_square
    else:
        # n is doubly even (divisible by 2 and 4 -> 4n)

        # Divide this square into four rectangles, each sized n/2 x n/4
        half_size = n // 2
        quarter_size = n // 4

        # Put these rectangles along each side of the square, at an offset of n/4
        coordinate_set = set()

        for i in range(half_size):
            for j in range(quarter_size):
                # Top rectangle
                coordinate_set.add((j, i + quarter_size))

                # Bottom rectangle
                coordinate_set.add((j + (n - quarter_size), i + quarter_size))

                # Left rectangle
                coordinate_set.add((i + quarter_size, j))

                # Right rectangle
                coordinate_set.add((i + quarter_size, j + (n - quarter_size)))

        # Initialize the counter
        counter = 1

        # Fill in the square
        for i in range(n):
            # If the coordinate is in one of the four rectangles, put in the counter normally,
            # else put in n^2 + 1 - counter
            for j in range(n):
                if (i, j) in coordinate_set:
                    magic_square[i][j] = counter
                else:
                    magic_square[i][j] = n**2 - counter + 1

                counter += 1

        return magic_square


if __name__ == "__main__":
    main()
