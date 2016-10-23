#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
# Authors:
# Jacek Wojdel <jacek.wojdel@skyscanner.net> - 2015
#
from engine.cell import Cell, DEAD


class LifeBoard:
    def __init__(self, args):
        self.size_x = args.size_x
        self.size_y = args.size_y
        self.board = {}

    def limit_pos(self, pos):
        return pos
        #return (pos[0] % self.size_x, pos[1] % self.size_y)
    
    def get_cell(self, x, y):
        limited_pos = self.limit_pos((x,y))
        try:
            return self.board[limited_pos]
        except KeyError:
            return None

    def all_cells(self):
        return set(self.board.values())
 
    def step(self):
        all_cells = self.all_cells()
        for cell in all_cells:
            cell.change_state()

        new_positions = set()
        for cell in all_cells:
            cell.calculate_change()
            if cell.is_alive:
                for x in range(cell.x - 1, cell.x + 2):
                    for y in range(cell.y - 1, cell.y + 2):
                        ncell = self.get_cell(x, y)
                        if ncell is None:
                            new_positions.add((x,y))
            elif cell.last_alive and cell.last_alive > 25:
                del self.board[(cell.x, cell.y)]

        for pos in new_positions:
            self.add_cell(pos[0], pos[1], DEAD)
            cell.calculate_change()
            
    def add_cell(self, x, y, state):
        cell = Cell(self, x, y, state)
        self.board[(x,y)] = cell
        return cell