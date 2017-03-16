from copy import deepcopy


class KnightsTourState:
    def __init__(self, knight_location, parent_state, n):
        self.n = n
        self.knight_location = knight_location
        self.neighbors = 0

        if parent_state is not None:
            self.visited_locations = deepcopy(parent_state.visited_locations)
            self.visited_locations.add(knight_location)
            self.starting_location = parent_state.starting_location
        else:
            self.starting_location = knight_location
            self.visited_locations = set()
        self.parent_state = parent_state

        # See how many neighbors this state has
        movement_tuples = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

        for m_t in movement_tuples:
            r, c = self.knight_location

            r += m_t[0]
            c += m_t[1]

            # If this point is on the board
            if 0 <= r < self.n and 0 <= c < self.n:
                square = r, c

                # Has this square been visited by the knight in this state yet?
                if square not in self.visited_locations:
                    self.neighbors += 1

    def __lt__(self, other):
        our_visited = len(self.visited_locations)
        their_visited = len(other.visited_locations)
        
        our_distance = abs(self.knight_location[0] - self.starting_location[0]) + abs(self.knight_location[1] - self.starting_location[1])
        their_distance = abs(other.knight_location[0] - other.starting_location[0]) + abs(other.knight_location[1] - other.starting_location[1])

        if our_visited == their_visited:
            if our_distance == their_distance:
                if self.neighbors != 0:
                    return self.neighbors < other.neighbors

                return False
            return our_distance > their_distance

        return our_visited > their_visited


