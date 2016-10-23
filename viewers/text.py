#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
# Authors:
# Jacek Wojdel <jacek.wojdel@skyscanner.net> - 2015
#


class TextViewer:
    def __init__(self, board, _args):
        self.board = board

    def display(self):
        separator = '+' + '-'*self.board.size_x + '|'
        print(separator)
        for y in range(self.board.size_y):
            line = '|'
            for x in range(self.board.size_x):
                cell = self.board.get_cell(x, y)
                try:
                    line += '#0OOOooooo........... '[cell.last_alive]
                except:
                    line += ' '
            line += '|'
            print(line)
        print(separator)

    def clear(self):
        print('\n' * 20)
    
    @classmethod
    def add_viewer_arguments(cls, _parser):
        pass
