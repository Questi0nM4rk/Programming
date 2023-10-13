import numpy as np
import sys

sys.setrecursionlimit(99999999)

"""
Chess annotation
qK{pos_to1}&{pos_to2}

exml:
    qKc4&e4
"""

#TODO:
# set number of children
# if false erase the knights that were placed on board
#

SIZE = 7
MOVES_X = [2, 1, -1, -2, -2, -1,  1,  2]
MOVES_Y = [1, 2,  2,  1, -1, -2, -2, -1]

class NomalKnight():
    
    def __init__(self, x, y, board, adds = 0) -> None:
        self.board = board
        self.last_move = ()
        counter = 2
        self.board[x,y] = 1
        print(self.solve(x, y, board, counter, adds))
        
    def solve(self, x, y, board, counter, adds):
        if counter >= adds:
            self.last_move = (x,y)
            return True

        for i in range(8):
            n_x = x + MOVES_X[i]
            n_y = y + MOVES_Y[i]
            if self.validate_move(n_x, n_y):
                self.board[n_x, n_y] = counter
                if self.solve(n_x, n_y, board, counter + 1, adds):
                    return True
                self.board[n_x, n_y] = 0
        return False
    
    def validate_move(self, x, y):
        if x < SIZE and x >= 0 and y < SIZE and y >= 0 and self.board[x, y] == 0:
            return True
        return False


"""
class BoostedKnight():
    path: list[str]
    board: list[list[bool]]

    def __init__(self, from_x, from_y, board) -> None:
        self.path = []
        self.board = board
        self.board[from_x][from_y] = True

        split = SIZE
        print(split)
        input()
        print(self.spawn_knights(from_x, from_y, split))

    def spawn_knights(self, x, y, split) -> bool:
        if self.check_board():
            return True

        if split <= 0:
            return False

        return False
    
    def validate_move(self, x: int, y: int):
        if x < 8 and x >= 0 and y < 8 and y >= 0 and self.board[x][y] == 0:
            return True
        return False

    def new_knight(self, x, y, split) -> bool:
        if not (0 <= x < SIZE and 0 <= y < SIZE): #and self.board[x][y] == 0):
            return False
        split -= 1
        print(split)
        return self.spawn_knights(x, y, split)

    def write_move(self, x1, y1, x2=None, y2=None):
        notation = "qK"
        if x2:
            notation += chr(ord("a") + x1) + str(y1+1) + "&" + chr(ord("a") + x2) + str(y1+1)
            self.board[x1][y1] = True
            self.board[x2][y1] = True
        elif y2:
            notation += chr(ord("a") + x1) + str(y1+1) + "&" + chr(ord("a") + x1) + str(y2+1)
            self.board[x1][y1] = True
            self.board[x1][y2] = True

        self.path.append(notation)
        
    def delete_moves(self, x1, y1, x2=None, y2=None):
        notation = "qK"
        if x2:
            notation += chr(ord("a") + x1) + str(y1+1) + "&" + chr(ord("a") + x2) + str(y1+1)
        elif y2:
            notation += chr(ord("a") + x1) + str(y1+1) + "&" + chr(ord("a") + x1) + str(y2+1)
            
        _from = self.path.index(notation)
        rem = self.path[:_from]
        self.path = self.path[:_from]
        
        for move in rem:
            move = move[2:]
            _first, _second = move.split("&")

            _first_x = int(ord(_first[0]) - ord("a"))
            _first_y = int(_first[1]) - 1

            _second_x = ord(_second[0]) - ord("a")
            _second_y = int(_second[1]) - 1
            
            self.board[_first_x][_first_y] = False
            self.board[_second_x][_second_y] = False
            
        
    def check_board(self) -> bool:
        return bool(np.all(self.board == 1))

"""
class BoostedKnight():
    def __init__(self, x, y, board) -> None:
        self.board = board


def validateMove(bo, row, col):
    if row < SIZE and row >= 0 and col < SIZE and col >= 0 and bo[row, col] == 0:
        return True

def solve (bo, row, col, counter):
    if counter >= 65:
        return True
    for i in range(8):
        new_x = row + MOVES_X[i]
        new_y = col + MOVES_Y[i]
        if validateMove(bo, new_x, new_y):
            bo[new_x,new_y] = counter
            if solve(bo,new_x, new_y, counter+1):
                return True
            bo[new_x,new_y] = 0
    return False


def main():
    
    board = np.zeros((SIZE, SIZE))
    #solve(board, 0, 0, 1)
    
    n_knight = NomalKnight(0,0,board)
    
    print(n_knight.board)
    """x,y = n_knight.last_move
    n2_knight = NomalKnight(x,y,n_knight.board, 1)
    
    print(n2_knight.board)"""
    
    """
    b_knight = BoostedKnight(0, 0, board)

    if b_knight.path:
        print("Path found!!!")
    print(b_knight.board)"""

if __name__ == "__main__":
    main()
