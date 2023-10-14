import os
import platform

from typing import Tuple, List
from tabulate import tabulate
from colorama import init, Fore, Back, Style


def waitForKey():
    if platform.system() == "Windows":
        os.system("pause")
    else:
        os.system("/bin/bash -c 'read -s -n 1 -p \"Press any key to continue...\"'")
        print()

def clearTerminal():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")
        print()


Position = Tuple[int, int]

class Visualizer:
    def __init__(self, size: int, path: List[Tuple[Position, Position, Position]], start: Position):
        self.size = size
        self.path = path
        self.start = start       
        self.board = [[False] * size for _ in range(size)]
        self.board[start[0]][start[1]] = True


    def run(self):
        self._drawBoard((-1,-1), (-1,-1), (-1,-1))
        for step in range(len(self.path)):
            (start, end1, end2) = self.path[step]
            self.board[start[0]][start[1]] = True
            self.board[end1[0]][end1[1]] = True
            self.board[end2[0]][end2[1]] = True
            self._drawBoard(start, end1, end2)
            waitForKey()
        clearTerminal()

    def _drawBoard(self, start, end1, end2):
        drawBoard(self.board, start, end1, end2)


def drawBoard(board, start, end1, end2):
    clearTerminal()
    formatted = [[
        (Fore.BLUE if (i,j) == end1 or (i,j) == end2 else Fore.RED if (i,j) == start else Fore.RESET) + "♞" + Fore.RESET if board[i][j] else (Back.RED if (i,j) == start else Back.RESET) + " " + Back.RESET 
    for i in range(len(board))] for j in range(len(board))]
    print(tabulate(formatted, tablefmt="fancy_grid"))
