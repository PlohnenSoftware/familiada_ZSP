cimport cython
from libc.math cimport floor

@cython.ccall
@cython.locals(surf_h=int, surf_w=int, offset=int, spacing=int, cols=int, rows=int)
def calc_grid_size(int surf_h, int surf_w, int offset, int spacing, int cols, int rows):
    """
    Calculate the size and position of a grid within a gray rectangle.

    Args:
        surf_h (int): Height of the surface.
        surf_w (int): Width of the surface.
        offset (int): Offset from the edges of the surface to the gray rectangle.
        spacing (int): Spacing between blocks in the grid.
        cols (int): Number of columns in the grid.
        rows (int): Number of rows in the grid.

    Returns:
        tuple: A tuple containing the following values:
            - start_x (float): The x-coordinate of the starting position of the grid.
            - start_y (float): The y-coordinate of the starting position of the grid.
            - font_size (int): The font size based on the block height.
            - block_width (float): The width of each block in the grid.
            - block_height (float): The height of each block in the grid.
            - rect_width (int): The width of the gray rectangle.
            - rect_height (int): The height of the gray rectangle.
    """
    cdef int rect_width, rect_height, font_size
    cdef double aspect_ratio_rect, aspect_ratio_grid, grid_width, block_width, block_height, grid_height_recalc
    cdef double start_x, start_y

    # Calculate dimensions for the gray rectangle
    rect_width = surf_w - 2 * offset
    rect_height = surf_h - 2 * offset

    # Aspect ratios
    aspect_ratio_rect = 1.5  # 3 / 2
    aspect_ratio_grid = 2.0  # 16 / 8

    # Calculate the maximum possible size of the grid within the gray rectangle
    if rect_width / rect_height > aspect_ratio_grid:
        grid_width = (rect_height - 2 * offset) * aspect_ratio_grid
    else:
        grid_width = rect_width - 2 * offset

    block_width = (grid_width - (cols - 1) * spacing) / cols
    block_height = block_width * aspect_ratio_rect
    grid_height_recalc = (block_height + spacing) * rows - spacing

    # Calculate the starting position of the grid
    start_x = offset + (rect_width - grid_width) / 2.0
    start_y = offset + (rect_height - grid_height_recalc) / 2.0
    font_size = max(round(block_height * 0.8), 2)  # Font size based on block height

    return (start_x, start_y, font_size, block_width, block_height, rect_width, rect_height)


@cython.ccall
@cython.locals(spa=cython.double, start_x=cython.double, start_y=cython.double, block_width=cython.double, block_height=cython.double, i=cython.int, j=cython.int)
def grid_creator_calc(double spa, double start_x, double start_y, double block_width, double block_height, int i, int j):
    """
    Calculates the coordinates and center of a rectangle in a grid.

    Parameters:
    spa (float): The spacing between each rectangle.
    start_x (float): The starting x-coordinate of the grid.
    start_y (float): The starting y-coordinate of the grid.
    block_width (float): The width of each rectangle.
    block_height (float): The height of each rectangle.
    i (int): The row index of the rectangle in the grid.
    j (int): The column index of the rectangle in the grid.

    Returns:
    tuple: A tuple containing the x-coordinate, y-coordinate, and center coordinates of the rectangle.
    """
    cdef double rect_x, rect_y
    cdef tuple coord_cent

    rect_x = start_x + j * (block_width + spa)
    rect_y = start_y + i * (block_height + spa)
    coord_cent = (rect_x + 0.55 * block_width, rect_y + 0.5 * block_height)

    return rect_x, rect_y, coord_cent


@cython.ccall
@cython.locals(no_answers=cython.int)
def calculate_coords(int no_answers) -> tuple:
    """
    Calculate the coordinates based on the number of answers.

    Parameters:
    - no_answers (int): The number of answers.

    Returns:
    - tuple: A tuple containing the number of answers and the row coordinates.
    """
    cdef int row_coords
    row_coords = 1 + max(int(floor((6 - no_answers) / 2)), 0)

    return no_answers, row_coords