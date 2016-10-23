#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
# Authors:
# Jacek Wojdel <jacek.wojdel@skyscanner.net> - 2015
#
import pygame


class SDLViewer:
    def __init__(self, board, args):
        self.board = board
        self.size_factor = args.pixel or 10
        self.create_color_function(args.color)

        pygame.display.init()
        self.screen = pygame.display.set_mode([self.size_factor * self.board.size_x * 4,
                                               self.size_factor * self.board.size_y * 4])
        self.screen.fill((0, 0, 0))
        pygame.display.update()

    def create_color_function(self, color):
        cap_range = lambda x: max(0, 255 - x * 10)
        if color == 'R':
            self.c_func = lambda x: (cap_range(x), 0, 0)
        elif color == 'G':
            self.c_func = lambda x: (0, cap_range(x), 0)
        else:
            self.c_func = lambda x: (0, 0, cap_range(x))
        
    def display(self):
        for cell in self.board.all_cells():
            x = cell.x + self.board.size_x
            y = cell.y + self.board.size_y
            if cell.is_alive:
                color = (255, 255, 255)
            else:
                age = cell.last_alive
                if age is not None:
                    color = self.c_func(age)
                else:
                    color = (0, 0, 0)
            pygame.draw.rect(self.screen, color, (x * self.size_factor, y * self.size_factor, self.size_factor, self.size_factor))

        pygame.display.update()

    def clear(self):
        pass

    @classmethod
    def add_viewer_arguments(cls, parser):
        parser.add_argument('-p', '--pixel', help='(X11 only) Pixel size', type=int, default=10)
        parser.add_argument('-c', '--color', help='(X11 only) Fading history color', choices='RGB', default='B')
