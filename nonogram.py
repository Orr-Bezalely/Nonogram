# -------------------------------〈 IMPORTS 〉------------------------------- #
import math
# -------------------------------〈 GLOBALS 〉------------------------------- #
BLACK = 1
WHITE = 0
UNKNOWN = -1
# -----------------------------〈 FUNCTIONS 〉------------------------------- #
def done(row, blocks, black_streak, block_num, index, black, unknown, total):
    """
    Checks whether a solution is correct or not and returns the corresponding
    boolean (None if it is indeterminable)
    :param row: list representing partial colouring of the row
    :param blocks: list representing the constraints of the row
    :param black_streak: integer representing number of consecutive blacks
    :param block_num: integer representing number of blocks so far
    :param index: integer representing position in row to check
    :param black: integer representing number of blacks
    :param unknown: integer representing number of unknowns
    :param total: integer representing the number of blacks there should be
    :return: boolean value if a solution is correct or not
    (None if indeterminable)
    """
    if black + unknown < total: return False
    if index == len(row):
        if black == total and block_num == len(blocks): return True
        else: return False
    if block_num > len(blocks): return False
    colour = row[index]
    if colour == WHITE and 0<black_streak<blocks[block_num - 1]: return False
    if colour == BLACK and black_streak == blocks[block_num - 1]: return False
    return None


def change_index(index, colour, new_row):
    """
    Gets index, colour and new row and changes the index to the correct colour
    returning the new row
    :param index: integer representing position in row to check
    :param colour: CONSTANT representing which colour to change to
    :param new_row: list representing a copy of the original row
    :return: list representing the new row with the colour adjustment
    """
    new_row[index] = colour
    return new_row


def unknown_colour(black_streak, block_size):
    """
    Gets the black streak and the block size and checks whether the unknown
    should be fixed to either colour or not
    :param black_streak: integer representing number of consecutive blacks
    :param block_size: integer representing the current block's size
    :return: tuple containing CONSTANT representing colour to change to and
    boolean representing whether the colour shouldn't be fixed
    """
    if (0 < black_streak < block_size): return BLACK, False
    elif black_streak == block_size: return WHITE, False
    else: return UNKNOWN, True


def row_var_helper(row, blocks, black_streak, block_num, index):
    """
    Runs recursively looking for solutions for the partially coloured row and
    returns all possible rows which satisfy the constraints
    :param row: list representing partial colouring of the row
    :param blocks: list representing the constraints of the row
    :param black_streak: integer representing number of consecutive blacks
    :param block_num: integer representing number of blocks so far
    :param index: integer representing position in row to check
    :return: 2-dimensional list containing all possible rows which satisfy the
    constraints
    """
    black, unknown, total = row.count(BLACK), row.count(UNKNOWN), sum(blocks)
    valid = done(row, blocks, black_streak, block_num, index, black,
                 unknown, total)
    if valid: return [row]
    elif valid == False: return []
    if black == total and unknown != 0:
        row = [i if i != UNKNOWN else WHITE for i in row]
    found, both, colour = [], False, row[index]
    if colour == UNKNOWN:
        colour, both = unknown_colour(black_streak, blocks[block_num - 1])
    if colour == WHITE or both == True:
        new_row_white = change_index(index, WHITE, row.copy())
        found.extend(row_var_helper(new_row_white, blocks, 0, block_num,
                                    index + 1))
    if colour == BLACK or both == True:
        new_row_black = change_index(index, BLACK, row.copy())
        if black_streak == 0:
            found.extend(row_var_helper(new_row_black, blocks, black_streak + 1
                                        , block_num + 1, index + 1))
        else:
            found.extend(row_var_helper(new_row_black, blocks, black_streak + 1
                                        , block_num, index + 1))
    return found


def get_row_variations(row, blocks):
    """
    Gets a row and returns all possible rows which satisfy the constraints of
    the blocks
    :param row: list representing partial colouring of the row
    :param blocks: list representing the constraints of the row
    :return: 2-dimensional list containing all possible rows which satisfy the
    constraints of the blocks
    """
    if blocks == [] and row.count(BLACK) > 0: return []
    return row_var_helper(row, blocks, 0, 0, 0)


def get_intersection_row(rows):
    """
    Gets a 2-dimensional list containing all possible rows which satisfy the
    constraints of the blocks and returns a list which represents the
    intersection of the possible rows.
    :param rows: 2-dimensional list containing all possible rows which satisfy
    the constraints of the blocks
    :return: list which represents the intersection of the possible rows.
    """
    if len(rows) == 0: return []
    return [i[0] if i.count(i[0]) == len(i) else UNKNOWN for i in invert(rows)]


def invert(board):
    """
    Transposes a 2-dimension list
    :param board: 2-dimensional list representing the board
    :return: 2-dimensional list representing the transposed board
    """
    return [list(i) for i in zip(*board)]


def create_board(rows, columns):
    """
    Creates a board filled with UNKNOWN with "rows" rows and "columns" columns
    :param rows: number representing number of rows in the board to be created
    :param columns: number representing number of columns in the board to be
    created
    :return: 2-dimensional list filled with UNKNOWN
    """
    return [[UNKNOWN]*len(columns)]*len(rows)


def solve_easy_nonogram(constraints):
    """
    Gets a 3-dimensional list representing the constraints and returns the
    most advanced logical deduction that can be derived from the constraints.
    :param constraints: 3-dimensional list containing vertical constraints and
    horizontal constraints
    :return: 2-dimensional list containing most advanced logical deduction
    that can be derived from the constraints.
    """
    board = create_board(constraints[0], constraints[1])
    return run_until_not_changed(board, constraints)


def get_dict(constraints):
    """
    Gets a list of constraints and returns a list of dictionaries, each having
    keys of row/column number and values of whether each row/column needs to be
    checked or not
    :param constraints: 3-dimensional list containing vertical constraints and
    horizontal constraints
    :return: list of dictionaries, each having keys of row/column number and
    values of whether each row/column needs to be checked or not
    """
    return [dict((j, True) for j in range(len(constraints[i]))) 
            for i in range(len(constraints))]


def change_dict(list_of_dicts, row, new_row):
    """
    Gets the list of dictionaries, old row and new row and checks where the
    row has been altered, changing each corresponding row's value in the
    dictionary to True
    :param list_of_dicts: list of dictionaries, each having keys of row/column
    number and values of whether each row/column needs to be checked or not
    :param row: list representing old partial colouring of the row
    :param new_row: list representing new partial colouring of the row
    :return: None
    """
    for item in range(len(new_row)):
        if new_row[item] != row[item]:
            list_of_dicts[0][item] = True


def run_until_not_changed(board, constraints):
    """
    Gets a 2-dimensional list representing the board and a 3-dimensional list
    representing the constraints and returns the most advanced logical
    deduction that can be derived from the constraints.
    :param board: 2-dimensional list representing the board
    :param constraints: 3-dimensional list containing vertical constraints and
    horizontal constraints
    :return: 2-dimensional list containing most advanced logical deduction
    that can be derived from the constraints.
    """
    changed = True
    list_of_dicts = get_dict(constraints)
    while changed == True:
        changed = False
        for i in range(len(constraints)):
            for row in range(len(constraints[i])):
                if list_of_dicts[i][row]:
                    rows = get_row_variations(board[row], constraints[i][row])
                    new_row = get_intersection_row(rows)
                    if new_row == []: return None
                    if new_row != board[row]:
                        change_dict(list_of_dicts[::-1], board[row], new_row)
                        changed, board[row] = True, new_row
            board = invert(board)
    return board


def get_index_of_first_unknown(board):
    """
    Gets a 2-dimensional list representing the board and checks the first
    position where an UNKNOWN value appears returning it
    :param board: 2-dimensional list representing the board
    :return: tuple representing row and index of the first UNKNOWN value
    """
    for row in range(len(board)):
        for index in range(len(board[row])):
            if board[row][index] == UNKNOWN:
                return row, index


def solve_nonogram_helper(constraints, board):
    """
    Gets a list of constraints and a board and recursively finds all the
    possible colourings of the board, returning them
    :param constraints: 3-dimensional list containing vertical constraints and
    horizontal constraints
    :param board: 2-dimensional list representing the board
    :return: list representing all the possible colourings of the board
    """
    board = run_until_not_changed(board, constraints)
    if board == None: return []
    first_unknown = get_index_of_first_unknown(board)
    if first_unknown == None: return [board]
    results, new_board_white, new_board_black = [], board.copy() ,board.copy()
    new_board_white[first_unknown[0]][first_unknown[1]] = WHITE
    results.extend(solve_nonogram_helper(constraints, new_board_white))
    new_board_black[first_unknown[0]][first_unknown[1]] = BLACK
    results.extend(solve_nonogram_helper(constraints, new_board_black))
    return results


def solve_nonogram(constraints):
    """
    Creates the board based on the constraints and returns all possible boards
    which satisfy all constraints
    :param constraints: 3-dimensional list containing vertical constraints and
    horizontal constraints
    :return: 3-dimensional list containing all possible board arrangements
    which satisfy all constraints
    """
    board = create_board(constraints[0], constraints[1])
    return solve_nonogram_helper(constraints, board)


def combinations(n, k):
    """
    Calculates the number of ways of choosing unordered subsets of k elements
    from a fixed set of n elements
    :param n: integer representing number of positions to choose from
    :param k: integer representing number of free zeros
    :return: integer representing number of different combinations of choosing
    unordered subsets of k elements from a fixed set of n elements
    """
    return math.factorial(n)//math.factorial(k)//math.factorial(n-k)


def ways(row, blocks, black_streak, block_num, index, black, unknown, total):
    """
    Runs recursively looking for solutions for the partially coloured row and
    returns number of possible combinations of the partially coloured row
    :param row: list representing partial colouring of the row
    :param blocks: list representing the constraints of the row
    :param black_streak: integer representing number of consecutive blacks
    :param block_num: integer representing number of blocks so far
    :param index: integer representing position in row to check
    :param black: integer representing number of blacks
    :param unknown: integer representing number of unknowns
    :param total: integer representing the number of blacks there should be
    :return: integer representing the number of possible combinations of the
    partially coloured row
    """
    valid = done(row, blocks, black_streak, block_num, index, black,
                 unknown, total)
    if valid: return 1
    elif valid == False: return 0
    if unknown == len(row[index:]) and black_streak == 0:
        return count_row_variations(unknown, blocks[block_num:])
    count, both, colour = 0, False, row[index]
    if colour == UNKNOWN:
        colour, both = unknown_colour(black_streak, blocks[block_num - 1])
        unknown -= 1
    if colour == WHITE or both == True:
        count += ways(row, blocks, 0, block_num, index + 1, black,
                      unknown, total)
    if colour == BLACK or both == True:
        if black_streak == 0:
            count += ways(row, blocks, black_streak + 1, block_num + 1,
                          index + 1, black + 1, unknown, total)
        else:
            count += ways(row, blocks, black_streak + 1, block_num,
                          index + 1, black + 1, unknown, total)
    return count


def count_row_variations(length, blocks, row=None):
    """
    Gets length, blocks and optional row and returns how many possible
    colourings of it there are
    :param length: integer representing length of row
    :param blocks: list representing the constraints of the row
    :param row: optional: list representing partial colouring of the row
    :return: integer representing number of possible colourings for the row
    """
    zero_num = length-sum(blocks)-(len(blocks)-1)
    group_size = len(blocks) + zero_num
    if group_size < zero_num or group_size < 0 or zero_num < 0: return 0
    if row == None: return combinations(group_size, zero_num)
    else: return ways(row, blocks, 0, 0, 0, 0, row.count(UNKNOWN), sum(blocks))


# --------------------------------〈 MAIN 〉--------------------------------- #
rows = [[3, 1, 5], [3, 1, 5, 1], [3, 6, 1], [3, 6, 5], [3, 2, 5, 5], [2, 7, 3, 4], [5, 1, 1], [1, 1, 1, 3, 3], [5, 1, 1], [8, 4, 2], [6, 1, 9, 1], [1, 1, 1, 11], [3, 5, 3],
[4, 4], [3, 2, 1, 1, 4], [6, 3, 1], [9, 2, 2, 1], [3, 4, 1, 2], [3, 2, 3], [3, 3, 6, 3], [4, 3, 11, 3], [9, 11, 3], [3, 10, 3, 3], [1, 1, 1, 4, 5], [5, 1, 3]]
columns = [[6, 1, 2, 2], [6, 1, 2, 5], [5, 4, 4, 4], [4, 1, 4, 4], [5, 4, 1], [4, 2, 3], [2, 3, 1, 5], [2, 3, 5, 1, 5], [1, 1, 7], [8, 3, 1, 3], [8, 7, 3, 1], [8, 8, 5],
[7, 4, 1, 5], [3, 1, 1, 4, 6], [1, 3, 5], [4, 1, 4], [2, 3, 5], [3, 3, 2, 3], [1, 3, 4, 6], [3, 5, 4], [3, 3, 9], [3, 1, 4, 2], [3, 2, 7], [1, 1, 1, 3], [4, 1, 3]]
# 25x25 Nonograms Puzzle ID: 8,179,093

#columns = [[1],[1,1],[1,2,2,3],[1,2,1,4],[2,2,4,2],[1,1,1,4],[2,3,2,1],[4,6],[1,1,2,1],[1,1,1,1,1],[2,1,2],[1,3,3],[1,2,2],[3,2],[4]]
#rows = [[4],[3],[3,2],[3,1],[7],[1,2,2],[5,2,2],[1,1],[1,1,5],[2,3,2],[1,1,1],[1,1,2,1],[2,7,1],[1,2,1,5],[1,2,3,4]]


#columns = [[2,4], [4], [2,1], [3,1], [2,1,1],[2,2,1],[2,2,1,1],[1,2,2],[1,1,2],[1,2,1]]
#rows = [[1,4],[2,4],[5],[4,2],[2,5],[1,4,1],[1],[1],[2],[6]]

constraints = [rows,columns]
x = solve_nonogram(constraints)
for row in x[0]:
    print(row)