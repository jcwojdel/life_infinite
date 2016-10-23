#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
# Authors:
# Jacek Wojdel <jacek.wojdel@skyscanner.net> - 2015
import unittest
from unittest.mock import MagicMock, patch

from engine.cell import Cell, ALIVE, DEAD


class Test(unittest.TestCase):
    def test_cell_alive(self):
        c = Cell(None, 0, 0, ALIVE)
        self.assertTrue(c.is_alive)

        c = Cell(None, 0, 0, DEAD)
        self.assertFalse(c.is_alive)

    def test_cell_neighbours(self):
        board_mock = MagicMock()
        c = Cell(board_mock, 3, 5)
        for _ in c.neighbours():
            pass

        self.assertEqual(board_mock.get_cell.call_count, 8)
        x_list = [args[0] for args, _kwargs in board_mock.get_cell.call_args_list]
        y_list = [args[1] for args, _kwargs in board_mock.get_cell.call_args_list]
        self.assertEqual(min(x_list), 2)
        self.assertEqual(max(x_list), 4)
        self.assertEqual(min(y_list), 4)
        self.assertEqual(max(y_list), 6)

    def test_count_neighbours(self):
        board_mock = MagicMock()
        acell = Cell(None, 0, 0, ALIVE)
        dcell = Cell(None, 0, 0, DEAD)
        board_mock.get_cell = MagicMock(side_effect=[acell, acell, acell, acell, acell, dcell, dcell, dcell])
        c = Cell(board_mock, 3, 5)
        self.assertEqual(c.get_alive_neighbours_count(), 5)

    def run_state_change_with_neighbours_count(self, cell, neighbours_count):
        with patch.object(cell, 'get_alive_neighbours_count') as count_mock:
            count_mock.return_value = neighbours_count
            cell.calculate_change()
            cell.change_state()

    def assert_dies(self, cell, neighbours_count):
        cell.state = ALIVE
        self.run_state_change_with_neighbours_count(cell, neighbours_count)
        self.assertFalse(cell.is_alive)

    def assert_spawns(self, cell, neighbours_count):
        cell.state = DEAD
        self.run_state_change_with_neighbours_count(cell, neighbours_count)
        self.assertTrue(cell.is_alive)

    def assert_unchanged(self, cell, neighbours_count):
        cell.state = ALIVE
        self.run_state_change_with_neighbours_count(cell, neighbours_count)
        self.assertTrue(cell.is_alive)

        cell.state = DEAD
        self.run_state_change_with_neighbours_count(cell, neighbours_count)
        self.assertFalse(cell.is_alive)

    def test_calculate_change(self):
        c = Cell(None, 3, 5)
        for count in [0, 1, 4, 5, 6, 7, 8]:
            self.assert_dies(c, count)

        self.assert_spawns(c, 3)

        self.assert_unchanged(c, 2)

if __name__ == "__main__":
    unittest.main()
