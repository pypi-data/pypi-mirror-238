#!/usr/bin/env python3

import unittest

from git_viewer import main

unittest.util._MAX_LENGTH=1000

class DetailsViewTests(unittest.TestCase):

	maxDiff = None

	def test_mark_links_one_line(self):
		markup = [('0-default:default', '* '), ('0-red:default', '7f710c9'), ('0-default:default', ' -^ -h '), ('0-green:default', '(5 days ago) '), ('1-blue:default', '<erzo>')]
		expected = [('0-default:default', '* '), ('color.link.hash', '7f710c9'), ('0-default:default', ' -^ -h '), ('0-green:default', '(5 days ago) '), ('1-blue:default', '<erzo>')]
		expected_number_links = 1
		actual, actual_number_links = main.DetailsView.mark_links_one_line(None, markup)
		self.assertListEqual(expected, actual)
		self.assertEqual(expected_number_links, actual_number_links)
	
	def test__get_markup__commit(self):
		markup = [('color.title', ['commit 4ed0fa9f34f3dd9b1ef7e05b65c813b6d67a420c', ' (', ('color.title.commit.refnames.head', 'HEAD'), ('color.title.commit.refnames.head-branch-sep', ' -> '), ('color.title.commit.refnames.branch.local', 'dev'), ')'])]
		expected = [('color.title', 'commit 4ed0fa9f34f3dd9b1ef7e05b65c813b6d67a420c ('), ('color.title.commit.refnames.head', 'HEAD'), ('color.title.commit.refnames.head-branch-sep', ' -> '), ('color.title.commit.refnames.branch.local', 'dev'), ('color.title', ')')]
		actual = main.DetailsLineView(markup).get_markup()
		self.assertEqual(expected, actual)

	def test__get_markup__intro(self):
		markup = ['using ', ('color.text.cmd', '`cursor down`'), ' ', [('default', '['), ('color.text.key', '<down>'), ' or ', ('color.text.key', 'j'), ']'], ' and ', ('color.text.cmd', '`cursor up`'), ' ', [('default', '['), ('color.text.key', '<up>'), ' or ', ('color.text.key', 'k'), ']']]
		expected = [(None, 'using '), ('color.text.cmd', '`cursor down`'), (None, ' '), ('default', '['), ('color.text.key', '<down>'), (None, ' or '), ('color.text.key', 'j'), (None, '] and '), ('color.text.cmd', '`cursor up`'), (None, ' '), ('default', '['), ('color.text.key', '<up>'), (None, ' or '), ('color.text.key', 'k'), (None, ']')]
		actual = main.IntroLineView(markup).get_markup()
		self.assertListEqual(expected, actual)


class ParseKeyTest(unittest.TestCase):

	def test__parse_key__one_simple_key(self):
		key_str = 'h'
		expected_key_list = ['h']
		actual_key_list = main.App.parse_key(key_str)
		self.assertListEqual(expected_key_list, actual_key_list)

	def test__parse_key__several_simple_keys(self):
		key_str = 'abc'
		expected_key_list = ['a', 'b', 'c']
		actual_key_list = main.App.parse_key(key_str)
		self.assertListEqual(expected_key_list, actual_key_list)


	def test__parse_key__one_special_key(self):
		key_str = '<enter>'
		expected_key_list = ['enter']
		actual_key_list = main.App.parse_key(key_str)
		self.assertListEqual(expected_key_list, actual_key_list)

	def test__parse_key__with_modifier(self):
		key_str = '<shift ctrl f5>'
		expected_key_list = ['shift ctrl f5']
		actual_key_list = main.App.parse_key(key_str)
		self.assertListEqual(expected_key_list, actual_key_list)

	def test__parse_key__multiple_with_modifier(self):
		key_str = '<ctrl w><ctrl w>'
		expected_key_list = ['ctrl w', 'ctrl w']
		actual_key_list = main.App.parse_key(key_str)
		self.assertListEqual(expected_key_list, actual_key_list)

	def test__parse_key__multiple_mixed(self):
		key_str = 'y<left>'
		expected_key_list = ['y', 'left']
		actual_key_list = main.App.parse_key(key_str)
		self.assertListEqual(expected_key_list, actual_key_list)


	def test__parse_key__less(self):
		key_str = '<less>'
		expected_key_list = ['<']
		actual_key_list = main.App.parse_key(key_str)
		self.assertListEqual(expected_key_list, actual_key_list)

	def test__parse_key__greater(self):
		key_str = '<greater>'
		expected_key_list = ['>']
		actual_key_list = main.App.parse_key(key_str)
		self.assertListEqual(expected_key_list, actual_key_list)

	def test__parse_key__space(self):
		key_str = '<space>'
		expected_key_list = [' ']
		actual_key_list = main.App.parse_key(key_str)
		self.assertListEqual(expected_key_list, actual_key_list)


	def test__parse_key__ctrl_space(self):
		key_str = '<<0>>'
		expected_key_list = ['<0>']
		actual_key_list = main.App.parse_key(key_str)
		self.assertListEqual(expected_key_list, actual_key_list)


if __name__ == '__main__':
	unittest.main()
