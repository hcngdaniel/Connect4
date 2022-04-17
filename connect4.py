#!/usr/bin/env python3
import typing
import numpy as np
from scipy.ndimage import convolve


class Connect4:

    none_symbol = " "
    none_id = 0
    white_symbol = "●"
    white_id = 1
    black_symbol = "◯"
    black_id = -1

    h = 6
    w = 7

    def __init__(self) -> None:
        self.board = [[self.none_id for _ in range(self.w)] for _ in range(self.h)]
        self.symbol_dict = {
            self.none_id: self.none_symbol,
            self.white_id: self.white_symbol,
            self.black_id: self.black_symbol,
        }
        self.turn = self.white_id

    def __str__(self) -> str:
        return "\n".join(["|" + "|".join(map(lambda x: self.symbol_dict[x], self.board[i])) + "|" for i in range(self.h)]) + "\n" + "-" * (self.w * 2 + 1)

    @property
    def legal_moves(self) -> typing.List[int]:
        return list(filter(lambda x: 0 in [self.board[i][x] for i in range(self.h)], [i for i in range(self.w)]))

    def move(self, col: int) -> None:
        if col not in self.legal_moves:
            raise ValueError(f"column {col} is not a legal move")
        if self.is_win() != self.none_id:
            raise RuntimeError("someone won this game already")
        self.board[self.h - [self.board[i][col] for i in range(self.h - 1, -1, -1)].index(0) - 1][col] = self.turn
        if self.turn == self.white_id:
            self.turn = self.black_id
        elif self.turn == self.black_id:
            self.turn = self.white_id

    def is_win(self) -> int:
        board = np.array(self.board)

        # check horizontally
        kernel = np.array([[1, 1, 1, 1]])
        conv = convolve(board, kernel, mode='constant')
        if 4 * self.white_id in conv:
            return self.white_id
        if 4 * self.black_id in conv:
            return self.black_id

        # check vertically
        kernel = np.array([[1],
                           [1],
                           [1],
                           [1]])
        conv = convolve(board, kernel, mode='constant')
        if 4 * self.white_id in conv:
            return self.white_id
        if 4 * self.black_id in conv:
            return self.black_id

        # check diagonally
        kernel = np.array([[1, 0, 0, 0],
                           [0, 1, 0, 0],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1]])
        conv = convolve(board, kernel, mode='constant')
        if 4 * self.white_id in conv:
            return self.white_id
        if 4 * self.black_id in conv:
            return self.black_id

        kernel = np.array([[0, 0, 0, 1],
                           [0, 0, 1, 0],
                           [0, 1, 0, 0],
                           [1, 0, 0, 0]])
        conv = convolve(board, kernel, mode='constant')
        if 4 * self.white_id in conv:
            return self.white_id
        if 4 * self.black_id in conv:
            return self.black_id

        return self.none_id
