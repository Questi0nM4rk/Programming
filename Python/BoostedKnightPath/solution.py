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

SIZE = 8        # The size of the board
MOVES_X = [2, 1, -1, -2, -2, -1,  1,  2]
MOVES_Y = [1, 2,  2,  1, -1, -2, -2, -1]

class NormalKnight():
    
    def __init__(self, board) -> None:
        self.last_move = ()
        self.board = board
        
    def solve(self, x, y, split):

        if not self.board[x][y]:
            self.board[x][y] = True

        for i in range(8):
            n_x = x + MOVES_X[i]
            n_y = y + MOVES_Y[i]
            if self.validate_move(n_x, n_y):
                self.board[n_x, n_y] = True
                if BoostedKnight(self.board).solve(n_x, n_y, split-1):
                    return True
                self.board[n_x, n_y] = False
        return False
    
    def validate_move(self, x, y):
        if x < SIZE and x >= 0 and y < SIZE and y >= 0 and self.board[x, y] == 0:
            return True
        return False


class BoostedKnight():
    def __init__(self, board) -> None:
        self.board = board
        self.path = []
        
    def solve(self, x, y, split) -> bool:
        if split == 0:
            return True

        k1 = NormalKnight(self.board).solve(x,y,split)
        k2 = NormalKnight(self.board).solve(x,y,split)
        
        if k1 and k2:
            #self.write_move()
            return True
        return False
    
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
        
        
"""
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
"""

def main():
    
    board = np.zeros((SIZE, SIZE))  # change to board size is done at the top
    
    boostedK = BoostedKnight(board) 
    boostedK.solve(0,0,7)           # x, y, number of splits the knight should make
    
    print(boostedK.board)


if __name__ == "__main__":
    main()
