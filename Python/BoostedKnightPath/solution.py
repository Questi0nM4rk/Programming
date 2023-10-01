import numpy as np

"""
Chess annotation
qK{pos_to1}&{pos_to2}

exml:
    qKc4&e4
"""

SIZE = 8
MOVES = [
    [2, (1, -1)],
    [-2, (1, -1)],
    [(1, -1), 2],
    [(1, -1), -2]
]



class BoostedKnight():
    Path: list[str]
    Board: list[int]

    def __init__(self, from_x, from_y, counter, board) -> None:
        self.Path = []
        self.Board = board
        self.Board[from_x][from_y] = counter

        self.spawn_knights(from_x, from_y, counter)


    def spawn_knights(self, x, y, counter) -> bool:
        
        for move in MOVES:
            if counter >= 6:
                return True

            if move[0] == 2 or move[0] == -2:
                new_x = x + move[0]
                new_y1 = y + move[1][0]
                new_y2 = y + move[1][1]
                
                if self.new_knight(new_x, new_y1, counter + 1) and self.new_knight(new_x, new_y2, counter + 1):
                    self.write_move(new_x, y1=new_y1, y2=new_y2)
                    return True
            else:
                new_x1 = x + move[0][0]
                new_x2 = x + move[0][1]
                new_y = y + move[1]

                if self.new_knight(new_x1, new_y, counter + 1) and self.new_knight(new_x2, new_y, counter + 1):
                    self.write_move(x1=new_x1, x2=new_x2, y1=new_y)
                    return True

        if x < SIZE:
            self.spawn_knights(x + 1, y, counter)
            
        elif x >= SIZE and y < SIZE:
            self.spawn_knights(0, y + 1, counter)

        self.Path.pop()
        return False


    def new_knight(self, x, y, counter) -> bool:
        if not (0 <= x < SIZE and 0 <= y < SIZE and self.Board[x][y] == 0):
            return False
        return self.spawn_knights(x, y, counter)


    def write_move(self, x1, y1, x2 = None, y2 = None):
        notation = "qK"
        if x2:
            notation += chr(ord("a") + x1) + str(y1) + "&" + chr(ord("a") + x2) + str(y1)
        elif y2:
            notation += chr(ord("a") + x1) + str(y1) + "&" + chr(ord("a") + x1) + str(y2)
        
        self.Path.append(notation)



def main():
    board = np.zeros((SIZE, SIZE))
    b_knight = BoostedKnight(0, 0, 1, board)

    if b_knight.Path:
        print("Path found!!!")


if __name__ == "__main__":
    main()
