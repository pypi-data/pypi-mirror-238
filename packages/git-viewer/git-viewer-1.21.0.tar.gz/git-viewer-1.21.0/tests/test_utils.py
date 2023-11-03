#!/usr/bin/env python3

import unittest
import re

from git_viewer import utils

unittest.util._MAX_LENGTH=1000

class UtilsTest(unittest.TestCase):

	maxDiff = None


	def setUp(self):
		self.colors = set()


	# ------- table -------

	def test_format_table(self):
		rows = [
			("Author/Committer: ", "me"),
			("Date: ",             "06.11.2021"),
		]
		expected = [
			"Author/Committer: me        ",
			"Date:             06.11.2021",
		]
		actual = utils.format_table(rows, col_sep="")
		self.assertListEqual(expected, actual)

	def test_format_table_one_fmt(self):
		rows = [
			("Author",         "me"),
			("Author Date",    "06.11.2021"),
			("Committer",      "somebody else"),
			("Committer Date", "07.11.2021"),
		]
		expected = [
			"Author:         me           ",
			"Author Date:    06.11.2021   ",
			"Committer:      somebody else",
			"Committer Date: 07.11.2021   ",
		]
		actual = utils.format_table(rows, fmt=["%s:"])
		self.assertListEqual(expected, actual)


	# ------- join -------

	def test_list_join_len_zero(self):
		sep = ", "
		list_in = []
		expected = []
		actual = utils.list_join(sep, list_in)
		self.assertListEqual(expected, actual)

	def test_list_join_len_one(self):
		sep = ", "
		list_in = [1]
		expected = [1]
		actual = utils.list_join(sep, list_in)
		self.assertListEqual(expected, actual)

	def test_list_join_len_two(self):
		sep = ", "
		list_in = ["a", "b"]
		expected = ["a", sep, "b"]
		actual = utils.list_join(sep, list_in)
		self.assertListEqual(expected, actual)

	def test_list_join_markup(self):
		sep = ("color.title", ", ")
		list_in = [("color.tag", "tag: v0.13.0"), ("color.branch-remote", "origin/master"), ("color.branch-local", "master")]
		expected = [("color.tag", "tag: v0.13.0"), sep, ("color.branch-remote", "origin/master"), sep, ("color.branch-local", "master")]
		actual = utils.list_join(sep, list_in)
		self.assertListEqual(expected, actual)


	# ------- replace in markup -------

	def test__replace_in_markup__str_str_str(self):
		cmd = "help --settings"
		markup = "`{cmd}`"
		expected = markup.replace("{cmd}", cmd)
		actual = utils.replace_in_markup(markup, "{cmd}", cmd)
		self.assertEqual(expected, actual)

	def test__replace_in_markup__str_reo_str__empty(self):
		markup = ""
		reo = re.compile("foo")
		actual = utils.replace_in_markup(markup, reo, "bar")
		expected = markup
		self.assertEqual(expected, actual)

	def test__replace_in_markup__str_reo_str__none(self):
		markup = "test"
		reo = re.compile("foo")
		actual = utils.replace_in_markup(markup, reo, "bar")
		expected = markup
		self.assertEqual(expected, actual)

	def test__replace_in_markup__str_reo_str__complete(self):
		markup = "foo"
		reo = re.compile("foo")
		actual = utils.replace_in_markup(markup, reo, "bar")
		expected = "bar"
		self.assertEqual(expected, actual)

	def test__replace_in_markup__str_reo_str__one(self):
		markup = "xfoox"
		reo = re.compile("foo")
		actual = utils.replace_in_markup(markup, reo, "bar")
		expected = "xbarx"
		self.assertEqual(expected, actual)

	def test__replace_in_markup__str_reo_str__two(self):
		markup = "xfoofoox"
		reo = re.compile("foo")
		actual = utils.replace_in_markup(markup, reo, "bar")
		expected = "xbarbarx"
		self.assertEqual(expected, actual)


	def test__replace_in_markup__str_reo_tuple__complete(self):
		markup = "foo"
		reo = re.compile("foo")
		actual = utils.replace_in_markup(markup, reo, ("attr", "bar"))
		expected = ("attr", "bar")
		self.assertEqual(expected, actual)

	def test__replace_in_markup__str_reo_tuple__suffix(self):
		markup = "foox"
		reo = re.compile("foo")
		actual = utils.replace_in_markup(markup, reo, ("attr", "bar"))
		expected = [("attr", "bar"), "x"]
		self.assertEqual(expected, actual)


	def test__replace_in_markup__str_reo_func_str(self):
		markup = "You can disable the visual mode again with `cancel` or `visual --toggle`."
		reo = re.compile('`(?P<cmd>.*?)`')
		def insert_shortcuts(m):
			cmd = m.group('cmd')
			if cmd == 'cancel':
				shortcut = '<esc>'
			elif cmd == 'visual --toggle':
				shortcut = 'V'
			else:
				shortcut = ''
			if shortcut:
				shortcut = " [%s]" % shortcut
			return m.group(0) + shortcut
		actual = utils.replace_in_markup(markup, reo, insert_shortcuts)
		expected = "You can disable the visual mode again with `cancel` [<esc>] or `visual --toggle` [V]."
		self.assertEqual(expected, actual)

	def test__replace_in_markup__str_reo_func_tuple(self):
		markup = "You can disable the visual mode again with `cancel` or `visual --toggle`."
		reo = re.compile('`(?P<cmd>.*?)`')
		def insert_shortcuts(m):
			out = ('color.cmd', m.group(0))
			cmd = m.group('cmd')
			if cmd == 'cancel':
				shortcut = '<esc>'
			elif cmd == 'visual --toggle':
				shortcut = 'V'
			else:
				shortcut = ''
			if shortcut:
				shortcut = " [%s]" % shortcut
				out = [out, ('color.key', shortcut)]
			return out
		actual = utils.replace_in_markup(markup, reo, insert_shortcuts)
		expected = ["You can disable the visual mode again with ", ("color.cmd", "`cancel`"), ("color.key", " [<esc>]"), " or ", ("color.cmd", "`visual --toggle`"), ("color.key", " [V]"), "."]
		self.assertEqual(expected, actual)


	def test__replace_in_markup__tuple_reo_str_tuple(self):
		markup = ("cmd", "`cmd`")
		expected = ("cmd", "`visual --toggle`")
		actual = utils.replace_in_markup(markup, re.compile("cmd"), "visual --toggle")
		self.assertEqual(expected, actual)

	def test__replace_in_markup__list_reo_str_list(self):
		markup = ['using ', ('color.text.cmd', '`{cmd}`'), ' ', [('default', '['), ('color.text.key', '{key1}'), ' or ', ('color.text.key', 'j'), ']'], ' and ', ('color.text.cmd', '`cursor up`'), ' ', [('default', '['), ('color.text.key', '<up>'), ' or ', ('color.text.key', 'k'), ']']]
		expected = ['using ', ('color.text.cmd', '`cursor down`'), ' ', [('default', '['), ('color.text.key', '<down>'), ' or ', ('color.text.key', 'j'), ']'], ' and ', ('color.text.cmd', '`cursor up`'), ' ', [('default', '['), ('color.text.key', '<up>'), ' or ', ('color.text.key', 'k'), ']']]

		actual = markup
		actual = utils.replace_in_markup(actual, re.compile("{cmd}"), "cursor down")
		actual = utils.replace_in_markup(actual, re.compile("{key1}"), "<down>")

		self.assertEqual(expected, actual)

	# ------- simplify markup -------

	def test__simplify_markup__str(self):
		markup = "hello world"
		expected = markup
		actual = utils.simplify_markup(markup)
		self.assertEqual(expected, actual)

	def test__simplify_markup__tuple_str(self):
		markup = ("red", "hello world")
		expected = markup
		actual = utils.simplify_markup(markup)
		self.assertEqual(expected, actual)

	def test__simplify_markup__tuple_tuple(self):
		markup = ("red", ("green", "hello world"))
		expected = ("green", "hello world")
		actual = utils.simplify_markup(markup)
		self.assertEqual(expected, actual)

	def test__simplify_markup__tuple_list(self):
		markup = ("red", ["hello ", ("green", "world")])
		expected = [("red", "hello "), ("green", "world")]
		actual = utils.simplify_markup(markup)
		self.assertEqual(expected, actual)

	def test__simplify_markup__list(self):
		markup = ["hello ", ("green", "world")]
		expected = [(None, "hello "), ("green", "world")]
		actual = utils.simplify_markup(markup)
		self.assertEqual(expected, actual)

	def test__simplify_markup__list_merge_same_attributes(self):
		markup = ['using ', ('color.text.cmd', '`cursor down`'), ' ', [('default', '['), ('color.text.key', '<down>'), ' or ', ('color.text.key', 'j'), ']'], ' and ', ('color.text.cmd', '`cursor up`'), ' ', [('default', '['), ('color.text.key', '<up>'), ' or ', ('color.text.key', 'k'), ']']]
		expected = [(None, 'using '), ('color.text.cmd', '`cursor down`'), (None, ' '), ('default', '['), ('color.text.key', '<down>'), (None, ' or '), ('color.text.key', 'j'), (None, '] and '), ('color.text.cmd', '`cursor up`'), (None, ' '), ('default', '['), ('color.text.key', '<up>'), (None, ' or '), ('color.text.key', 'k'), (None, ']')]
		actual = utils.simplify_markup(markup)
		self.assertEqual(expected, actual)

	# ------- replace attributes -------

	def test__replace_attribute__str(self):
		markup = "foo"
		expected_markup = markup
		expected_number = 0
		actual_markup, actual_number = utils.replace_attribute(markup, "cmd", "cmd-link")
		self.assertEqual(expected_markup, actual_markup)
		self.assertEqual(expected_number, actual_number)

	def test__replace_attribute__tuple_0(self):
		markup = ("default", "foo")
		expected_markup = markup
		expected_number = 0
		actual_markup, actual_number = utils.replace_attribute(markup, "cmd", "cmd-link")
		self.assertEqual(expected_markup, actual_markup)
		self.assertEqual(expected_number, actual_number)

	def test__replace_attribute__tuple_1(self):
		markup = ("cmd", "foo")
		expected_markup = ("cmd-link", "foo")
		expected_number = 1
		actual_markup, actual_number = utils.replace_attribute(markup, "cmd", "cmd-link")
		self.assertEqual(expected_markup, actual_markup)
		self.assertEqual(expected_number, actual_number)

	def test__replace_attribute__list_0(self):
		markup = [("default", "["), ("key", "f"), "]"]
		expected_markup = markup
		expected_number = 0
		actual_markup, actual_number = utils.replace_attribute(markup, "cmd", "cmd-link")
		self.assertEqual(expected_markup, actual_markup)
		self.assertEqual(expected_number, actual_number)

	def test__replace_attribute__list_1(self):
		markup = [("default", "`"), ("cmd", "f"), "`"]
		expected_markup = [("default", "`"), ("cmd-link", "f"), "`"]
		expected_number = 1
		actual_markup, actual_number = utils.replace_attribute(markup, "cmd", "cmd-link")
		self.assertEqual(expected_markup, actual_markup)
		self.assertEqual(expected_number, actual_number)

	def test__replace_attribute__list_nested(self):
		markup = ["a", ("color1", ["b", ("color2", ["c", ("cmd", "`help`")])])]
		expected_markup = ["a", ("color1", ["b", ("color2", ["c", ("cmd-link", "`help`")])])]
		expected_number = 1
		actual_markup, actual_number = utils.replace_attribute(markup, "cmd", "cmd-link")
		self.assertEqual(expected_markup, actual_markup)
		self.assertEqual(expected_number, actual_number)

	def test__replace_attribute__list_flat(self):
		markup = ["a", ("cmd", "`config.export`"), ("cmd", "`config.edit`"), ("cmd", "`config.load`"), ("color2", "hello world"), "b"]
		expected_markup = ["a", ("cmd-link", "`config.export`"), ("cmd-link", "`config.edit`"), ("cmd-link", "`config.load`"), ("color2", "hello world"), "b"]
		expected_number = 3
		actual_markup, actual_number = utils.replace_attribute(markup, "cmd", "cmd-link")
		self.assertEqual(expected_markup, actual_markup)
		self.assertEqual(expected_number, actual_number)

	# ------- replace_to_markup -------

	def test_replace_to_markup_split_once(self):
		ln_in = "a, b, c, d"
		expected = ["a", ": ", "b, c, d"]
		actual = utils.replace_to_markup(ln_in, ", ", ": ", count=1)
		self.assertListEqual(expected, actual)

	def test_replace_to_markup_split_all(self):
		ln_in = "a, b, c, d"
		old_sep = ", "
		new_sep = ": "
		expected = ["a", new_sep, "b", new_sep, "c", new_sep, "d"]
		actual = utils.replace_to_markup(ln_in, old_sep, new_sep)
		self.assertListEqual(expected, actual)

	def test_replace_to_markup_no_split(self):
		ln_in = "commit {hash_id}"
		expected = [ln_in]
		actual = utils.replace_to_markup(ln_in, "{refnames}", "HEAD -> master")
		self.assertListEqual(expected, actual)

	def test_replace_to_markup(self):
		ln_in = "commit {hash_id}{refnames}"
		refnames = [("color.head", "HEAD"), ("color.head-sep", " -> "), ("color.branch", "master")]
		expected = ["commit {hash_id}"] + refnames
		actual = utils.replace_to_markup(ln_in, "{refnames}", refnames)
		self.assertListEqual(expected, actual)

	def test_replace_to_markup__markup_function__new_list(self):
		ln_in = "commit {hash_id}{refnames}"
		refnames = "HEAD -> master, origin/master, tag: v13"
		def markup(deco):
			if deco.startswith("HEAD"):
				return ("color.head", deco)
			elif deco.startswith("origin/"):
				return ("color.branch-remote", deco)
			elif deco.startswith("tag: "):
				return ("color.tag", deco)
			else:
				return deco

		old_sep = ", "
		new_sep = " "
		refnames_expected = [("color.head", "HEAD -> master"), new_sep, ("color.branch-remote", "origin/master"), new_sep, ("color.tag", "tag: v13")]
		expected = ["commit {hash_id}"] + refnames_expected

		refnames = utils.replace_to_markup(refnames, old_sep, new_sep, markup_function=markup)
		actual = utils.replace_to_markup(ln_in, "{refnames}", refnames)

		self.assertListEqual(expected, actual)


	# ------- palette tuples <-> color strings -------

	def test__palette_tuple_to_color_str__fg(self):
		palette_tuple = ("error", "dark red", "default")
		expected_color_str = "red/default"
		actual_color_str = utils.palette_tuple_to_color_str(palette_tuple)
		self.assertEqual(expected_color_str, actual_color_str)

		regenerated_palette_tuple = utils.color_str_to_palette_tuple("error", expected_color_str)
		self.assertEqual(palette_tuple, regenerated_palette_tuple)

	def test__palette_tuple_to_color_str__emph(self):
		palette_tuple = ("subtitle", "white,bold", "default")
		expected_color_str = "bright white,bold/default"
		actual_color_str = utils.palette_tuple_to_color_str(palette_tuple)
		self.assertEqual(expected_color_str, actual_color_str)

		regenerated_palette_tuple = utils.color_str_to_palette_tuple("subtitle", expected_color_str)
		self.assertEqual(palette_tuple, regenerated_palette_tuple)

	def test__palette_tuple_to_color_str__bg(self):
		palette_tuple = ("test", "default", "dark magenta")
		expected_color_str = "default/magenta"
		actual_color_str = utils.palette_tuple_to_color_str(palette_tuple)
		self.assertEqual(expected_color_str, actual_color_str)

		regenerated_palette_tuple = utils.color_str_to_palette_tuple("test", expected_color_str)
		self.assertEqual(palette_tuple, regenerated_palette_tuple)

	def test__color_str_to_palette_tuple__no_bg(self):
		name = "error"
		color_str = "red"
		expected_palette_tuple = ("error", "dark red", "default")
		actual_palette_tuple = utils.color_str_to_palette_tuple(name, color_str)
		self.assertEqual(expected_palette_tuple, actual_palette_tuple)


	# ------- colored_str_to_markup -------

	def define_color(self, color):
		if color.startswith('%') and color.endswith('%'):
			return color[1:-1]
		self.colors.add(color)
		return color

	def test_colored_str_to_markup_empty(self):
		ln = ""
		expected = ""
		actual = utils.colored_str_to_markup(ln, self.define_color)
		self.assertEqual(expected, actual)
		self.assertEqual(set(), self.colors)

	def test_colored_str_to_markup_str(self):
		ln = "abc"
		expected = "abc"
		actual = utils.colored_str_to_markup(ln, self.define_color)
		self.assertEqual(expected, actual)
		self.assertEqual(set(), self.colors)

	def test_colored_str_to_markup_one_color(self):
		ln = "hello <color=red>world</color>"
		expected = ["hello ", ("red", "world")]
		actual = utils.colored_str_to_markup(ln, self.define_color)
		self.assertEqual(expected, actual)
		self.assertEqual({"red"}, self.colors)

	def test_colored_str_to_markup_nested_colors(self):
		ln = "<color=green>hello <color=red>world</color></color>"
		expected = ("green", ["hello ", ("red", "world")])
		actual = utils.colored_str_to_markup(ln, self.define_color)
		self.assertEqual(expected, actual)
		self.assertEqual({"green", "red"}, self.colors)

	def test_colored_str_to_markup_chained_colors(self):
		ln = "a<color=yellow>b<color=red>c</color>d<color=green>e</color>f</color>g"
		expected = ["a", ("yellow", ["b", ("red", "c"), "d", ("green", "e"), "f"]), "g"]
		actual = utils.colored_str_to_markup(ln, self.define_color)
		self.assertEqual(expected, actual)
		self.assertEqual({"yellow", "red", "green"}, self.colors)

	def test_colored_str_to_markup_missing_closing_tag(self):
		ln = "hello <color=red>world"
		expected = ["hello ", ("red", "world")]
		actual = utils.colored_str_to_markup(ln, self.define_color)
		self.assertEqual(expected, actual)
		self.assertEqual({"red"}, self.colors)

	def test_colored_str_to_markup_missing_two_closing_tags(self):
		ln = "<color=red>hello <color=green>world"
		expected = ("red", ["hello ", ("green", "world")])
		actual = utils.colored_str_to_markup(ln, self.define_color)
		self.assertEqual(expected, actual)
		self.assertEqual({"red", "green"}, self.colors)

	def test_colored_str_to_markup_reference_other_color(self):
		ln = "<color=red>hello <color=%title%>world"
		expected = ("red", ["hello ", ("title", "world")])
		actual = utils.colored_str_to_markup(ln, self.define_color)
		self.assertEqual(expected, actual)
		self.assertEqual({"red"}, self.colors)


	# ------- mnemonics -------

	def test__command_with_mnemonic(self):
		mnemonic = 'p like in preferences'
		cmd = 'config.edit'
		cmd_with_mnemonic = utils.CommandWithMnemonic(cmd, mnemonic)
		self.assertIsInstance(cmd_with_mnemonic, str)
		self.assertEqual(cmd_with_mnemonic, str(cmd_with_mnemonic))
		self.assertEqual(cmd_with_mnemonic, cmd)
		self.assertEqual(cmd_with_mnemonic.mnemonic, mnemonic)

	def test__mnemonic(self):
		cmd = 'yank cwd' //utils.Mnemonic('yank path')
		self.assertEqual(cmd, 'yank cwd')
		self.assertEqual(cmd.mnemonic, 'yank path')

	def test__command_with_mnemonic__add_mnemonic(self):
		utils.Mnemonic.sep = ", "
		cmd = 'layout hor' //utils.Mnemonic('like in sway') + utils.Mnemonic('h is already assigned to `go left` and b is next to v')
		self.assertIsInstance(cmd, utils.CommandWithMnemonic)
		self.assertEqual(cmd, 'layout hor')
		self.assertEqual(cmd.mnemonic, 'like in sway, h is already assigned to `go left` and b is next to v')

	def test__command_with_mnemonic__add_str(self):
		cmd = 'set details-view.auto-open!'  //utils.Mnemonic('<ctrl space> is intercepted by the terminal to insert a null character')
		cmd += ' config.auto-reload!'
		self.assertIsInstance(cmd, str)
		self.assertEqual(cmd, 'set details-view.auto-open! config.auto-reload!')


	# ------- join -------

	def test__join__empty(self):
		l = tuple()
		expected = ''
		actual = utils.join(l, ', ', ' and ')
		self.assertEqual(expected, actual)

	def test__join__one(self):
		l = ('vim',)
		expected = 'vim'
		actual = utils.join(l, ', ', ' and ')
		self.assertEqual(expected, actual)

	def test__join__two(self):
		l = ('vim', 'ranger')
		expected = 'vim and ranger'
		actual = utils.join(l, ', ', ' and ')
		self.assertEqual(expected, actual)

	def test__join__three(self):
		l = ('vim', 'ranger', 'qutebrowser')
		expected = 'vim, ranger and qutebrowser'
		actual = utils.join(l, ', ', ' and ')
		self.assertEqual(expected, actual)

	def test__join__four(self):
		l = ('vim', 'ranger', 'qutebrowser', 'sway')
		expected = 'vim, ranger, qutebrowser and sway'
		actual = utils.join(l, ', ', ' and ')
		self.assertEqual(expected, actual)

if __name__ == '__main__':
	unittest.main()
