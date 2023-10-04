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

SIZE = 10
MOVES = [
    [2, (1, -1)],
    [-2, (1, -1)],
    [(1, -1), 2],
    [(1, -1), -2]
]


class BoostedKnight():
    path: list[str]
    board: list[list[bool]]

    def __init__(self, from_x, from_y, board) -> None:
        self.path = []
        self.board = board
        self.board[from_x][from_y] = True

        split = SIZE - 2
        print(split)
        input()
        print(self.spawn_knights(from_x, from_y, split))

    def spawn_knights(self, x, y, split) -> bool:
        if self.check_board():
            return True

        if split <= 0:
            return False

        for move in MOVES:

            if move[0] == 2 or move[0] == -2:
                new_x = x + move[0]
                new_y1 = y + move[1][0]
                new_y2 = y + move[1][1]

                if self.new_knight(new_x, new_y1, split) and self.new_knight(new_x, new_y2, split):
                    self.write_move(new_x, y1=new_y1, y2=new_y2)
                    return True
                
                else:
                    if not (0 <= x < SIZE and 0 <= y < SIZE and self.board[x][y] == 0):
                        self.board[new_x][new_y1] = False
                        self.board[new_x][new_y2] = False
                    split += 1

            else:
                new_x1 = x + move[0][0]
                new_x2 = x + move[0][1]
                new_y = y + move[1]

                if self.new_knight(new_x1, new_y, split) and self.new_knight(new_x2, new_y, split):
                    self.write_move(x1=new_x1, x2=new_x2, y1=new_y)
                    return True
                else:
                    if not (0 <= x < SIZE and 0 <= y < SIZE and self.board[x][y] == 0):
                        self.board[new_x1][new_y] = False
                        self.board[new_x2][new_y] = False
                    split += 1
            
        if self.path:
            self.path.pop()
        return False

    def new_knight(self, x, y, split) -> bool:
        if not (0 <= x < SIZE and 0 <= y < SIZE and self.board[x][y] == 0):
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


def main():
    
    board = np.zeros((SIZE, SIZE))
    b_knight = BoostedKnight(0, 0, board)

    if b_knight.path:
        print("Path found!!!")


if __name__ == "__main__":
    main()
