import numpy as np
from itertools import product
import sys
import time

sys.setrecursionlimit(99999999)

"""
Chess annotation
qK{pos_to1}&{pos_to2}

exml:
    qKc4&e4
"""

SIZE = 8
MOVES_X = [2 , 1, -1, -2, -2, -1, 1, 2]
MOVES_Y = [1, 2, 2, 1, -1 , -1, -2, -2, -1]



class NormalKnight():
    
    def __init__(self, board) -> None:
        self.last_move = ()
        self.board = board
        
    def solve(self, x, y, counter):

        if counter >= SIZE*SIZE:
            return True
        
        if not self.board[x][y]:
            self.board[x][y] = True

        for i in range(8):
            n_x = x + MOVES_X[i]
            n_y = y + MOVES_Y[i]
            if self.validate_move(n_x, n_y):
                self.board[n_x, n_y] = True
                if self.solve(n_x, n_y, counter+1):
                    return True
                self.board[n_x, n_y] = False
        return False
    
    def validate_move(self, x, y):
        if x < SIZE and x >= 0 and y < SIZE and y >= 0 and self.board[x, y] == 0:
            return True
        return False




KNIGHT_MOVES = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
SPLIT_MOVES = [(a,b) for (a,b) in product(KNIGHT_MOVES, KNIGHT_MOVES) if a != b]



class BoostedKnight():
    def __init__(self, size) -> None:
        self.board = np.zeros((size, size))
        self.path = []
        self.size = size


    def solve(self, x, y) -> bool:
        if self.size % 2 == 0:
            return False

        self.board[x][y] = True
        self.start = (x, y)
        if self._backtracking(1):
            return True
        
        return False
    
    
    def _backtracking(self, existingPieces):
        if existingPieces >= self.size ** 2:
            return True
        
        validMoves = self._getValidMoves()

        for start in validMoves.keys():
            for (end1, end2) in validMoves[start]:
                self.board[end1[0], end1[1]] = True
                self.board[end2[0], end2[1]] = True
                
                self._writeMove(start, end1, end2)
                
                if self._backtracking(existingPieces+2):
                    return True
                
                self.path.pop()

                self.board[end1[0], end1[1]] = False
                self.board[end2[0], end2[1]] = False

        return False


    def _getValidMoves(self):
        res = {}
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j]:
                    moves = self._getChildrenOfPiece(i, j)
                    if len(moves) > 0:
                        res[(i, j)] = moves
        return res
    
    
    def _getChildrenOfPiece(self, i, j):
        allMoves = [(
                (x1 + i, y1 + j),
                (x2 + i, y2 + j)
            ) for ((x1, y1), (x2, y2)) in SPLIT_MOVES 
        ]
        return [(x,y) for (x,y) in allMoves if self._isMoveValid(x, y)]
    
    
    def _isMoveValid(self, newPos1, newPos2):
        x1, y1 = newPos1
        x2, y2 = newPos2
        if min(x1, x2, y1, y2) < 0 or max(x1, x2, y1, y2) >= self.size:
            return False
        if self.board[x1][y1] or self.board[x2][y2]:
            return False
        return True
    
    
    def _writeMove(self, start, pos1, pos2):
        notation = f"{chr(ord('a') + start[0]) + str(int(start[1])+1)}qK"
        notation += chr(ord("a") + pos1[0]) + str(int(pos2[1])+1) + "&" + chr(ord("a") + pos2[0]) + str(int(pos2[1])+1)

        self.path.append(notation)
        
        
def main():
    size = 9
    
    start_time = time.time()
    boostedK = BoostedKnight(size) 
    boostedK.solve(0,0)
    end_time = time.time()

    print(boostedK.board)
    print(boostedK.path)
    print(end_time - start_time)


if __name__ == "__main__":
    main()
