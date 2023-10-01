import numpy as np

"""
Chess annotation
qK{pos_to1}&{pos_to2}

exml:
    qKc4&e4
"""

#TODO:
# set number of children
#
#

SIZE = 8
MOVES = [
    [2, (1, -1)],
    [-2, (1, -1)],
    [(1, -1), 2],
    [(1, -1), -2]
]


class BoostedKnight():
    path: list[str]
    board: list[int]

    def __init__(self, from_x, from_y, board) -> None:
        self.path = []
        self.board = board
        self.board[from_x][from_y] = True

        for y in range(SIZE):
            for x in range(SIZE):
                self.spawn_knights(x, y)

    def spawn_knights(self, x, y) -> bool:
        for move in MOVES:
            if self.check_board(): # change to board checker
                return True

            if move[0] == 2 or move[0] == -2:
                new_x = x + move[0]
                new_y1 = y + move[1][0]
                new_y2 = y + move[1][1]

                if self.new_knight(new_x, new_y1) and self.new_knight(new_x, new_y2):
                    self.write_move(new_x, y1=new_y1, y2=new_y2)
                    return True

            else:
                new_x1 = x + move[0][0]
                new_x2 = x + move[0][1]
                new_y = y + move[1]

                if self.new_knight(new_x1, new_y) and self.new_knight(new_x2, new_y):
                    self.write_move(x1=new_x1, x2=new_x2, y1=new_y)
                    return True

                self.board
            
            
        self.path.pop()
        return False

    def new_knight(self, x, y) -> bool:
        if not (0 <= x < SIZE and 0 <= y < SIZE and self.board[x][y] == 0):
            return False
        return self.spawn_knights(x, y)

    def write_move(self, x1, y1, x2=None, y2=None):
        notation = "qK"
        if x2:
            notation += chr(ord("a") + x1) + str(y1) + "&" + chr(ord("a") + x2) + str(y1)
            self.board[x1][y1] = True
            self.board[x2][y1] = True
        elif y2:
            notation += chr(ord("a") + x1) + str(y1) + "&" + chr(ord("a") + x1) + str(y2)
            self.board[x1][y1] = True
            self.board[x1][y2] = True

        self.path.append(notation)
        
    def check_board(self) -> bool:
        return bool(np.all(self.board == 1))


def main():
    board = np.zeros((SIZE, SIZE))
    b_knight = BoostedKnight(0, 0, board)

    if b_knight.path:
        print("Path found!!!")


if __name__ == "__main__":
    main()
