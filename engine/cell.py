#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
# Authors:
# Jacek Wojdel <jacek.wojdel@skyscanner.net> - 2015
#
DEAD = 0
ALIVE = 1


class Cell:
    def __init__(self, board, x, y, state=DEAD):
        self.board = board
        self.x = x
        self.y = y
        self.state = state
        self.future_state = None
        self.last_alive = None

    def neighbours(self):
        for x in range(self.x - 1, self.x + 2):
            for y in range(self.y - 1, self.y + 2):
                if x != self.x or y != self.y:
                    yield self.board.get_cell(x, y)

    def get_alive_neighbours_count(self):
        count = 0
        for c in self.neighbours():
            if c is not None and c.is_alive:
                count += 1
        return count

    @property
    def is_alive(self):
        return self.state == ALIVE

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, v):
        self._state = v
        if self._state == ALIVE:
            self.last_alive = 0

    def calculate_change(self):
        count = self.get_alive_neighbours_count()
        if count < 2:
            self.future_state = DEAD
        elif count == 3:
            self.future_state = ALIVE
        elif count > 3:
            self.future_state = DEAD
        else:
            self.future_state = self.state

    def change_state(self):
        if self.future_state is None:
            return

        self.state = self.future_state

        if not self.is_alive:
            try:
                self.last_alive += 1
            except:
                pass
