import numpy as np
"""
bachet_odd module

This module contains functions to generate and manipulate Bachet matrices, 
which have unique properties and patterns used in mathematical puzzles and studies.

Functions:
- bachet_matrix(n): Generate a Bachet matrix of order n.
- operations(mat, n): Perform a sequence of operations on a matrix.
- get_center_matrix(matrix): Extract the center part of a square matrix.
"""


def bachet_matrix(n: int) -> np.ndarray:
    """
    https://en.wikipedia.org/wiki/Claude_Gaspar_Bachet_de_M%C3%A9ziriac


    Generate the Bachet matrix of order n.

    The Bachet matrix is a square matrix of order `2n-1` with
    a unique property related to its construction pattern.

    Parameters:
    - n (int): The order of the desired Bachet matrix.

    Returns:
    - np.ndarray: The Bachet matrix of order `n`.

    >>> print(batchet_matrix(5))
    [[ 0  0  0  0  1  0  0  0  0]
     [ 0  0  0  2  0  6  0  0  0]
     [ 0  0  3  0  7  0 11  0  0]
     [ 0  4  0  8  0 12  0 16  0]
     [ 5  0  9  0 13  0 17  0 21]
     [ 0 10  0 14  0 18  0 22  0]
     [ 0  0 15  0 19  0 23  0  0]
     [ 0  0  0 20  0 24  0  0  0]
     [ 0  0  0  0 25  0  0  0  0]]
    >>>
    """

    # Define matrix size based on n.
    N = 2 * n - 1
    bach_matrix = np.zeros((N, N), dtype=int)

    # Initial row and column indices for the first diagonal.
    rows = np.arange(n)
    cols = np.arange(n - 1, -1, -1)

    # Initial values for the first diagonal.
    low = 1
    high = n + 1

    # Fill the matrix diagonally.
    for _ in range(n):
        bach_matrix[rows, cols] = range(low, high)
        rows += 1
        cols += 1
        low += n
        high += n

    return bach_matrix


def operations(mat: np.ndarray, n: int) -> np.ndarray:
    """
    Perform a sequence of operations on a matrix.

    This function applies a series of transformations on the input matrix `mat`,
    which includes segment-wise addition, flipping and transposing operations.

    The input matrix is assumed to have at least `n + n//2` rows.

    Parameters:
    - mat (np.ndarray): The input matrix.
    - n (int): Parameter determining the size of the segment for operations.

    Returns:
    - np.ndarray: The transformed matrix.

    Example:
	>>> n = 5
	>>> bachet = odd.bachet_matrix(n)
	>>> bachet_ops = odd.operations(bachet, n)
	>>> print(bachet_ops)
	[[ 0  0  0  0  1  0  0  0  0]
	 [ 0  0  0  2  0  6  0  0  0]
	 [ 0  0  3 20  7 24 11  0  0]
	 [ 0  4 16  8 25 12  4 16  0]
	 [ 5  0  9 21 13  5 17  0 21]
	 [ 0 10 22 14  1 18 10 22  0]
	 [ 0  0 15  2 19  6 23  0  0]
	 [ 0  0  0 20  0 24  0  0  0]
	 [ 0  0  0  0 25  0  0  0  0]]

    """

    m = n // 2

    # Apply operations in a loop.
    for _ in range(2):
        mat[n:n + m] += mat[:m]
        mat = np.flipud(mat)
        mat[n:n + m] += mat[:m]
        mat = mat.T

    # Final flipping operations.
    mat = np.fliplr(mat)
    mat = np.flipud(mat)

    return mat


def get_center_matrix(matrix: np.ndarray) -> np.ndarray:
    """
    Extract the center part of a square matrix.

    Given a square matrix, this function will return a submatrix
    which corresponds to the center part. The number of rows/columns
    skipped from the outer boundary is calculated as `(N+1)//4`
    where N is the number of rows/columns in the input matrix.

    Parameters:
    - matrix (np.ndarray): Input square matrix.

    Returns:
    - np.ndarray: The center submatrix.

    Example:
	>>> print(bachet_ops)
	[[ 0  0  0  0  1  0  0  0  0]
	 [ 0  0  0  2  0  6  0  0  0]
	 [ 0  0  3 20  7 24 11  0  0]
	 [ 0  4 16  8 25 12  4 16  0]
	 [ 5  0  9 21 13  5 17  0 21]
	 [ 0 10 22 14  1 18 10 22  0]
	 [ 0  0 15  2 19  6 23  0  0]
	 [ 0  0  0 20  0 24  0  0  0]
	 [ 0  0  0  0 25  0  0  0  0]]
	>>> center_matrix = odd.get_center_matrix(bachet_ops)
	>>> print(center_matrix)
	[[ 3 20  7 24 11]
	 [16  8 25 12  4]
	 [ 9 21 13  5 17]
	 [22 14  1 18 10]
	 [15  2 19  6 23]]

    """

    # Assuming matrix is square (N x N)
    N = matrix.shape[0]

    # Calculate the number of rows/columns to skip from the boundary.
    skip = (N + 1) // 4

    # Extract the center submatrix.
    center_matrix = matrix[skip:-skip, skip:-skip]

    return center_matrix
