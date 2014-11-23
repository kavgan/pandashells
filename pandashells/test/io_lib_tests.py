#! /usr/bin/env python
import os
import sys
import json
import pandas as pd
from unittest import TestCase
from pandashells.lib.module_checker_lib import check_for_modules
from pandashells.lib import io_lib
import argparse
from mock import patch, MagicMock, call
import StringIO

class IOLibTests(TestCase):
    def test_get_separator_csv(self):
        """
        get_separator() recognizes csv
        """
        config_dict = {'io_input_type': 'csv'}
        args = MagicMock(input_options=['csv'])
        self.assertEqual(',', io_lib.get_separator(args, config_dict))

    def test_get_separator_table(self):
        """
        get_separator() recognizes table
        """
        config_dict = {'io_input_type': 'csv'}
        args = MagicMock(input_options=['table'])
        self.assertEqual(r'\s+', io_lib.get_separator(args, config_dict))

    def test_get_separator_default(self):
        """
        get_separator() goes to default for unrecognized
        """
        config_dict = {'io_input_type': 'csv'}
        args = MagicMock(input_options=[])
        self.assertEqual(',', io_lib.get_separator(args, config_dict))

    def test_get_header_names_with_names_and_header(self):
        """
        get_header_names() does right thing for names and header
        """
        args = MagicMock(names=['a'], input_options=[])
        header, names = io_lib.get_header_names(args)
        self.assertEqual(header, 0)
        self.assertEqual(names, ['a'])

    def test_get_header_names_with_names_and_no_header(self):
        """
        get_header_names() does right thing for names and header
        """
        args = MagicMock(names=['a'], input_options=['noheader'])
        header, names = io_lib.get_header_names(args)
        self.assertEqual(header, None)
        self.assertEqual(names, ['a'])

    def test_get_header_names_with_no_names_and_header(self):
        """
        get_header_names() does right thing for names and header
        """
        args = MagicMock(names=None, input_options=[])
        header, names = io_lib.get_header_names(args)
        self.assertEqual(header, 'infer')
        self.assertEqual(names, None )

    def test_get_header_names_with_no_names_and_no_header(self):
        """
        get_header_names() does right thing for names and header
        """
        args = MagicMock(names=None, input_options=['noheader'])
        header, names = io_lib.get_header_names(args)
        self.assertEqual(header, None)
        self.assertEqual(names, None )

    @patch('pandashells.lib.io_lib.sys.stdin')
    @patch('pandashells.lib.io_lib.pd')
    def test_df_from_input_no_infile(self, pd_mock, stdin_mock):
        """
        """
        pd_mock.read_csv = MagicMock(return_value=pd.DataFrame())
        args = MagicMock(names=[], input_options=[])
        df = io_lib.df_from_input(args, in_file=None)
        self.assertEqual(pd_mock.read_csv.call_args_list[0][0][0], stdin_mock)

    @patch('pandashells.lib.io_lib.pd')
    def test_df_from_input_with_infile(self, pd_mock):
        """
        """
        pd_mock.read_csv = MagicMock(return_value=pd.DataFrame())
        args = MagicMock(names=[], input_options=[])
        in_file = MagicMock()
        df = io_lib.df_from_input(args, in_file=in_file)
        self.assertEqual(pd_mock.read_csv.call_args_list[0][0][0], in_file)

    @patch('pandashells.lib.io_lib.pd')
    def test_df_from_input_create_names(self, pd_mock):
        """
        """
        df_in = pd.DataFrame(columns=[1, 2])
        pd_mock.read_csv = MagicMock(return_value=df_in)
        pd_mock.Index = pd.Index
        args = MagicMock(names=[], input_options=['noheader'])
        df = io_lib.df_from_input(args, in_file=None)
        self.assertEqual(['c0', 'c1'], list(df.columns))

    @patch('pandashells.lib.io_lib.sys')
    def test_csv_writer(self, sys_mock):
        sys_mock.stdout =  StringIO.StringIO()
        df = pd.DataFrame([[1, 2], [3, 4]], columns=['a', 'b'], index=[0, 1])
        io_lib.csv_writer(df, header=True, index=False)
        sys.stdout = sys.__stdout__
        self.assertEqual('"a","b"\n1,2\n3,4\n', sys_mock.stdout.getvalue())

    @patch('pandashells.lib.io_lib.sys')
    def test_table_writer(self, sys_mock):
        sys_mock.stdout =  StringIO.StringIO()
        df = pd.DataFrame([[1, 2], [3, 4]], columns=['a', 'b'], index=[0, 1])
        io_lib.table_writer(df, header=True, index=False)
        sys.stdout = sys.__stdout__
        self.assertEqual(' a  b\n 1  2\n 3  4\n', sys_mock.stdout.getvalue())

    @patch('pandashells.lib.io_lib.sys')
    def test_html_writer(self, sys_mock):
        sys_mock.stdout =  StringIO.StringIO()
        df = pd.DataFrame([[1, 2], [3, 4]], columns=['a', 'b'], index=[0, 1])
        io_lib.html_writer(df, header=True, index=False)
        sys.stdout = sys.__stdout__
        html = sys_mock.stdout.getvalue()
        self.assertTrue('<th>a</th>' in html)
        self.assertTrue('<th>b</th>' in html)
        self.assertTrue('<td> 1</td>' in html)

    def test_df_to_output(self):
        print
        print '*'*80
        print 'I need to write this test and then make docstrings for all these tests'







