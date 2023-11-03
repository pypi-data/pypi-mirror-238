#!/usr/bin/env python3

import unittest

from git_viewer import model
LogModel = model.LogModel


class ModelTests(unittest.TestCase):

	maxDiff = None

	# ------- replace_characters_in_cmd -------

	def test_replace_characters_in_cmd_2_commands_all_occurences(self):
		cmd      = [["test", "* ^foo ^^", "* ^bar"]] * 2
		expected = [["test", "* foo ", "* bar"]] * 2
		actual = model.Model.replace_characters_in_cmd(cmd, "^", "")
		self.assertEqual(expected, actual)

	def test_replace_characters_in_cmd_2_commands_one_occurence(self):
		cmd      = [["test", "* ^foo ^^", "a^2 + b^2 = c^2"], ["^42", "E = mc^2"]]
		expected = [["test", "* foo ^^",  "a^2 + b^2 = c^2"], ["42",  "E = mc^2"]]
		actual = model.Model.replace_characters_in_cmd(cmd, "^", "", 1)
		self.assertEqual(expected, actual)

	def test_replace_characters_in_cmd_single_command_all_occurences(self):
		cmd      = ["test", "* ^foo ^^", "* ^bar"]
		expected = ["test", "* foo ", "* bar"]
		actual = model.Model.replace_characters_in_cmd(cmd, "^", "")
		self.assertEqual(expected, actual)

	def test_replace_characters_in_cmd_single_command_one_occurence(self):
		cmd      = ["test", "* ^foo ^^", "a^2 + b^2 = c^2"]
		expected = ["test", "* foo ^^",  "a^2 + b^2 = c^2"]
		actual = model.Model.replace_characters_in_cmd(cmd, "^", "", 1)
		self.assertEqual(expected, actual)

	# ------- append_cmd_log --no-graph -------

	def test_append_cmd_log_no_graph(self):
		cmd_bak = LogModel.cmd_log

		LogModel.cmd_log = ['git', 'log', '--color', '--graph']
		expected_cmd_log = ['git', 'log', '--color']
		LogModel.append_cmd_log(['--no-graph'])
		self.assertEqual(expected_cmd_log, LogModel.cmd_log)

		LogModel.cmd_log = cmd_bak

	def test_append_cmd_log_no_graph_without_graph(self):
		cmd_bak = LogModel.cmd_log

		LogModel.cmd_log = ['git', 'log', '--color']
		expected_cmd_log = ['git', 'log', '--color']
		LogModel.append_cmd_log(['--no-graph'])
		self.assertEqual(expected_cmd_log, LogModel.cmd_log)

		LogModel.cmd_log = cmd_bak

	def test_append_cmd_log_no_graph_multiple_graph(self):
		cmd_bak = LogModel.cmd_log

		LogModel.cmd_log = ['git', 'log', '--color', '--graph', '--graph']
		expected_cmd_log = ['git', 'log', '--color']
		LogModel.append_cmd_log(['--graph', '--graph', '--no-graph'])
		self.assertEqual(expected_cmd_log, LogModel.cmd_log)

		LogModel.cmd_log = cmd_bak

	def test_append_cmd_log_no_graph_respect_order(self):
		cmd_bak = LogModel.cmd_log

		LogModel.cmd_log = ['git', 'log', '--color', '--graph']
		expected_cmd_log = ['git', 'log', '--color', '--graph']
		LogModel.append_cmd_log(['--no-graph', '--graph'])
		self.assertEqual(expected_cmd_log, LogModel.cmd_log)

		LogModel.cmd_log = cmd_bak

	# ------- insert_align_char -------

	def test_insert_align_char_after_one_ansi_escape(self):
		color = "[36m"
		ln = color + "* test"
		expected = color + "* ^test"
		actual = model.DetailsModel.insert_align_char(ln, 2)
		self.assertEqual(expected, actual)

	def test_insert_align_char_after_two_ansi_escapes(self):
		color = "[31m"
		color_reset = "[m"
		ln = color + "*" + color_reset + " test"
		expected = color + "*" + color_reset + " ^test"
		actual = model.DetailsModel.insert_align_char(ln, 2)
		self.assertEqual(expected, actual)

	def test_insert_align_char_before_escape(self):
		color = "[32m"
		ln = color + "* test"
		expected = model.ALIGN_CHAR + color + "* test"
		actual = model.DetailsModel.insert_align_char(ln, 0)
		self.assertEqual(expected, actual)

	def test_insert_align_char_empty(self):
		ln = ""
		expected = model.ALIGN_CHAR
		actual = model.DetailsModel.insert_align_char(ln, 2)
		self.assertEqual(expected, actual)


if __name__ == '__main__':
	unittest.main()
