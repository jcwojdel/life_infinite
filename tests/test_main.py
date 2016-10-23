#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
# Authors:
# Jacek Wojdel <jacek.wojdel@skyscanner.net> - 2015
import unittest
import life
from engine.exceptions import IncorrectArguments


class TestMainModule(unittest.TestCase):

    def test_parse_size_args(self):
        args = life.parse_arguments(['-s', '60x40'])
        self.assertEqual(args.size_x, 60)
        self.assertEqual(args.size_y, 40)

    def test_parse_size_default_args(self):
        args = life.parse_arguments([])
        self.assertEqual(args.size_x, 20)
        self.assertEqual(args.size_y, 20)

    def test_parse_size_incorrect_args(self):
        incorrect_values = ['0x40', '40x0', '40x-50', '10x', '100', 'x10']
        for v in incorrect_values:
            with self.assertRaises(IncorrectArguments, msg='Failed to raise on size: {}'.format(v)):
                args = life.parse_arguments(['-s', v])

if __name__ == "__main__":
    unittest.main()