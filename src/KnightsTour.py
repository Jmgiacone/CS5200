from KnightsTourState import KnightsTourState
from queue import PriorityQueue
import time


def main():
    output_file = open("knights_tour_results.txt", "w")
    total_start = time.time()
    for i in [8, 12, 16, 20]:
        print("Running closed knight's tour on {}x{}".format(i, i))
        start = time.time()
        stack = knights_tour(i, (i // 2, i // 2))
        end = time.time()
        delta = end - start

        print("Elapsed time: {} microseconds ({} seconds)".format(delta * 1000000, delta))
        output_file.write("Closed knight's tour on {}x{}\n".format(i, i))
        output_file.write("Elapsed time: {} microseconds ({} seconds)\n".format(delta * 1000000, delta))

        if stack is not None:
            # Write to output file

            output_file.write("Solution:\n")
            while len(stack) != 0:
                state = stack.pop()

                output_file.write(get_current_board_string(state, i) + "\n")
        else:
            output_file.write("Impossible\n")

        print()

    total_end = time.time()

    delta = total_end - total_start

    print("Total elapsed time: {} microseconds ({} seconds)".format(delta * 1000000, delta))
    output_file.write("Total elapsed time: {} microseconds ({} seconds)".format(delta * 1000000, delta))


def knights_tour(n, starting_square):
    movement_tuples = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

    # Create a start state
    start_state = KnightsTourState(starting_square, None, n)

    # Implement a best-first search
    frontier = PriorityQueue()
    frontier.put(start_state)

    # Set of visited states
    visited = set()

    while not frontier.empty():
        # Treat this list as a queue
        current_state = frontier.get()

        # This state is now visited
        visited.add(current_state)

        # Check if we've visited every square and we ended up back where we started
        if len(current_state.visited_locations) == n ** 2 and \
                        current_state.knight_location == current_state.starting_location:
            ptr = current_state
            stack = []

            while ptr is not None:
                stack.append(ptr)
                ptr = ptr.parent_state

            return stack

        # Generate every move the knight can make from its current position
        for m_t in movement_tuples:
            r, c = current_state.knight_location

            r += m_t[0]
            c += m_t[1]

            # If this point is on the board
            if 0 <= r < n and 0 <= c < n:
                square = r, c

                # Has this square been visited by the knight in this state yet?
                if square not in current_state.visited_locations:
                    neighbor = KnightsTourState(square, current_state, n)

                    if neighbor not in visited:
                        frontier.put(neighbor)

    # Exhausted all states and haven't found a solution. Impossible
    return None


def get_current_board_string(state, n):
    """Prints the current board using pretty ASCII art
    Note: you can delete this function if you wish
    """

    total_output = ""

    # iterate through the range in reverse order
    for r in range(n+1, -2, -1):
        output = ""
        if r == n+1 or r == 0:
            # then the top or bottom of the board
            output = "   +"
            output = ((len(str(n-1)) - 1) * " ") + output
            for i in range(n):
                output += "---"

            output += "+"
        elif r == -1:
            # then show the ranks
            output = "     "
            x = len(str(n-1))
            for i in range(n):
                output += str(i).zfill(x) + (" " * (2-x+1))
        else:  # board
            output = " " + str(n - r).zfill(len(str(n-1))) + " |"
            # fill in all the files with pieces at the current rank
            for file_offset in range(0, n):
                # start at a, with with file offset increasing the char
                f = file_offset

                code = "."  # default "no piece"

                if (n - r, f) == state.knight_location:
                    code = "K"
                elif (n - r, f) == state.starting_location:
                    code = "S"
                elif (n - r, f) in state.visited_locations:
                    code = "x"

                output += " " + code + " "

            output += "|"
        total_output += output + "\n"
    return total_output

if __name__ == "__main__":
    main()