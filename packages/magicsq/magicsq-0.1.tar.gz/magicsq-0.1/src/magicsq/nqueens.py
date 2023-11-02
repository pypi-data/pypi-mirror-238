class NQueensSolver:

    def __init__(self, n):
        self.n = n
        self.solutions = []

    def solve(self):
        """
        Solve the N-Queens problem and store the solutions in the `solutions` attribute.
        """
        self.solutions = list(self._queens(self.n))

    def _queens(self, n, i=0, *args):
        """
        A generator that yields all the possible placements for n queens on an nxn chessboard such that no two queens threaten each other.

        Parameters:
        - n (int): The size of the chessboard (i.e., n x n).
        - i (int): The current row being considered.
        - *args: Lists used to keep track of the columns and diagonals already being attacked by previously placed queens.

        Returns:
        - list of int: The column positions of the queens for a particular solution.
        """
        a, b, c = args if args else ([], [], [])  # Lists for column, diagonal1, diagonal2 attacks
        if i < n:
            for j in range(n):
                if j not in a and i + j not in b and i - j not in c:
                    yield from self._queens(n, i + 1, a + [j], b + [i + j], c + [i - j])
        else:
            yield a

    def display_solutions(self, counts):
        """
        Display all the solutions for the N-Queens problem.
        """
        cnt = 0
        for solution in self.solutions:
            if cnt == counts:
                break
            cnt += 1
            self._display_chessboard(solution)
            print([i + 1 for i in solution], "\n")  # Display the numerical positions

    def _display_chessboard(self, queens_positions):
        """
        Prints a visual representation of the chessboard with queens placed as per the provided solution.

        Parameters:
        - queens_positions (list of int): A list where each element represents the column position of the queen in the corresponding row.

        Returns:
        - None
        """
        n = len(queens_positions)
        divider = '+' + '--+' * n

        for row in range(n):
            print(divider)
            row_data = []
            for col in range(n):
                if queens_positions[col] == row:
                    row_data.append(' Q')
                else:
                    row_data.append('  ')
            print('|' + '|'.join(row_data) + '|')
        print(divider)

