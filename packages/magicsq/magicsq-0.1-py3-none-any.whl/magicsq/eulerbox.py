import numpy as np

"""
eulerbox module

This module focuses on creating magic square matrices based on a specific date or given values. 
It utilizes Euler's box method to generate a 4x4 magic square with distinct properties.

Functions:
- magicsquare(date, values_list, random): Calculate a magic square matrix based on a given date.
"""


class EulerMagicBox:
    """
    This class is designed to produce a "Magic Square" matrix based on a given date.
    The magic square is derived using a unique method that considers the day, month, and year
    of the date to produce a matrix which, when added to another matrix, gives meaningful values.
    """

    @classmethod
    def magicsquare(cls, date, values_list=None, random=False):
        """
        Calculate the magic square matrix based on a given date.

        Args:
        - date (str): The date string in 'dd-mm-yyYY' format.
        - values_list (list, optional): A list of four numbers to be mapped to 'p', 'q', 'r', and 's'. Defaults to [1, 2, 3, 4].
        - random (bool): If True, picks random values for 'p', 'q', 'r', and 's' from the range derived from the date.

        Returns:
        - numpy.ndarray: A 4x4 magic square matrix.
        """

        # Split the date into day, month, year
        dd, mm, yyYY = date.split('-')
        yy = int(yyYY[:2])
        YY = int(yyYY[2:])
        dd = int(dd)
        mm = int(mm)

        # Determine the sequence for p, q, r, s based on the sorted values of the date
        sorted_values = sorted([(dd, 'dd'), (mm, 'mm'), (yy, 'yy'), (YY, 'YY')])

        # If random is true, pick random values from a specified range
        if random:
            values_list = np.random.choice(range(min(dd, mm, yy, YY) - 1, max(dd, mm, yy, YY) + 1), 4,
                                           replace=False).tolist()
        elif values_list is None:
            values_list = [1, 2, 3, 4]

        mapping = {name: value for value, (num, name) in zip(values_list, sorted_values)}

        p = mapping['dd']
        q = mapping['mm']
        r = mapping['yy']
        s = mapping['YY']

        # Calculate M1 matrix based on the given date
        A = dd - p
        B = mm - q
        C = yy - r
        D = YY - s
        M1 = np.array([
            [A, B, C, D],
            [C, D, A, B],
            [D, C, B, A],
            [B, A, D, C]
        ])

        # Use a standard 4x4 arrangement for M2.
        M2 = np.array([
            [p, q, r, s],
            [s, r, q, p],
            [q, p, s, r],
            [r, s, p, q]
        ])

        # Calculate the sum matrix
        sum_matrix = M1 + M2

        # Check if any element in the final matrix is not greater than 0
        if (sum_matrix <= 0).any():
            return -1

        return sum_matrix


