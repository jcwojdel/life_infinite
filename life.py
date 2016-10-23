#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
# Authors:
# Jacek Wojdel <jacek.wojdel@skyscanner.net> - 2015
#
import argparse
import random
import time


from engine.exceptions import IncorrectArguments
from engine.board import LifeBoard
from viewers.text import TextViewer
from viewers.sdl import SDLViewer
from engine.cell import DEAD, ALIVE


VIEWER_MAPPING = {'TXT': TextViewer, 'X11': SDLViewer}

def parse_arguments(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--size', help='Initial size of the board', default='20x20')
    parser.add_argument('-n', '--num-steps', help='Number of steps', type=int, default=100)
    parser.add_argument('-r', '--random', help='Initialise random soup', action='store_true')
    parser.add_argument('-d', '--delay', help='Step delay', type=float, default=0.05)
    parser.add_argument('-f', '--file', help='Load initial state from file', action='append')
    parser.add_argument('-V', '--viewer', help='Viewer to be used', choices=['TXT', 'X11'], default='TXT')
    for viewer_type in VIEWER_MAPPING.values():
        viewer_type.add_viewer_arguments(parser)
    
    args = parser.parse_args(argv)
    try:
        args.size_x, args.size_y = (int(v) for v in args.size.split('x'))
    except Exception as e:
        raise IncorrectArguments(e)
    else:
        if args.size_x <= 0 or args.size_y <= 0:
            raise IncorrectArguments('Size must be >0 in both directions')

    return args


def randomize_board(board):
    for x in range(board.size_x):
        for y in range(board.size_y):
            if random.choice([DEAD, ALIVE]) == ALIVE:
                board.add_cell(x, y, ALIVE)


def load_board(board, fname):
    with open(fname) as f:
        y = 0
        for line in f:
            x = 0
            for c in line:
                if c == '#':
                    board.get_cell(x, y).state = ALIVE
                x += 1

            y += 1


def main():
    args = parse_arguments()
    board = LifeBoard(args)
    
    try:
        viewer = VIEWER_MAPPING[args.viewer](board, args)
    except KeyError:
        print('I don\'t know viewer: {}'.format(args.viewer))
        return -1
    except Exception as e:
        print('Failed to construct {} viewer with args {}'.format(args.viewer, args))

    if args.random:
        randomize_board(board)

    if args.file:
        for fname in args.file:
            load_board(board, fname)

    for _ in range(args.num_steps):
        board.step()
        viewer.clear()
        viewer.display()
        time.sleep(args.delay)

if __name__ == '__main__':
    main()
