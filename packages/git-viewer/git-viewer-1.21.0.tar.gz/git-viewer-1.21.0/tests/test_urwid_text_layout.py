#!/usr/bin/env python3

import unittest

from git_viewer.urwid_text_layout import LogTextLayout as TextLayout, calc_width, reverse_calc_text_pos


class TextLayoutTests(unittest.TestCase):

	maxDiff = None


	# ------- reverse_calc_text_pos -------

	def test_reverse_calc_text_pos(self):
		text = "123456789"
		width = 4
		expected = "6789"
		i0, sc = reverse_calc_text_pos(text, 0, len(text), width)
		actual = text[i0:]
		self.assertEqual(width, sc)
		self.assertEqual(expected, actual)

	def test_reverse_calc_text_pos_fullwidth(self):
		text = "日本語を使ってもいいですか？"
		width = 13
		expected = "いいですか？"
		expected_width = 12
		i0, sc = reverse_calc_text_pos(text, 0, len(text), width)
		actual = text[i0:]
		self.assertEqual(expected_width, sc)
		self.assertEqual(expected, actual)

	def test_reverse_calc_text_pos_line_long_enough(self):
		text = "日本語を使ってもいいですか？"
		width = 13
		expected = "いい"
		expected_width = 2*2
		i0 = 8
		i1 = 10
		i0, sc = reverse_calc_text_pos(text, i0, i1, width)
		actual = text[i0:i1]
		self.assertEqual(expected_width, sc)
		self.assertEqual(expected, actual)


	# ------- test half width characters -------

	def test_clip(self):
		text = " * 13f1c00 -^ (origin/dev) bugfix: subcommand map has higher priority than standard bindings (7 days ago)"
		width = 22
		broken_text = "\n".join(self.break_text(text, width, TextLayout.ALIGN_INDENTATION, TextLayout.WRAP_CLIP))
		expected = text.replace("^","")[:width]
		self.assertEqual(expected, broken_text)

	def test_ellipsis(self):
		text = " * 13f1c00 -^ (origin/dev) bugfix: subcommand map has higher priority than standard bindings (7 days ago)"
		expected = " * 13f1c00 - (origi..."
		broken_text = "\n".join(self.break_text(text, 22, TextLayout.ALIGN_INDENTATION, TextLayout.WRAP_ELLIPSIS, ellipsis_character="..."))
		self.assertEqual(expected, broken_text)

	def test_ellipsis_too_long(self):
		text = " * 13f1c00 -^ (origin/dev) bugfix: subcommand map has higher priority than standard bindings (7 days ago)"
		expected = " * 13f1c00 ..."
		broken_text = "\n".join(self.break_text(text, 14, TextLayout.ALIGN_INDENTATION, TextLayout.WRAP_ELLIPSIS, ellipsis_character="..."))
		self.assertEqual(expected, broken_text)

	def test_ellipsis_window_as_wide_as_ellipsis(self):
		text = " * 13f1c00 -^ (origin/dev) bugfix: subcommand map has higher priority than standard bindings (7 days ago)"
		expected = "..."
		broken_text = "\n".join(self.break_text(text, 3, TextLayout.ALIGN_INDENTATION, TextLayout.WRAP_ELLIPSIS, ellipsis_character="..."))
		self.assertEqual(expected, broken_text)

	def test_ellipsis_much_too_long(self):
		text = " * 13f1c00 -^ (origin/dev) bugfix: subcommand map has higher priority than standard bindings (7 days ago)"
		expected = "56789"
		broken_text = "\n".join(self.break_text(text, 5, TextLayout.ALIGN_INDENTATION, TextLayout.WRAP_ELLIPSIS, ellipsis_character="123456789"))
		self.assertEqual(expected, broken_text)

	def test_ellipsis_much_too_long_fullwidth(self):
		text = " * 13f1c00 -^ (origin/dev) bugfix: subcommand map has higher priority than standard bindings (7 days ago)"
		expected = "スト"
		broken_text = "\n".join(self.break_text(text, 5, TextLayout.ALIGN_INDENTATION, TextLayout.WRAP_ELLIPSIS, ellipsis_character="テスト".encode('utf-8')))
		self.assertEqual(expected, broken_text)

	def test_custom_wrap_after(self):
		# test that the line is broken after both wrap_after_characters
		# and else where if there are no wrap_after_characters
		# and that it does not break at wrap_after_characters if there is still enough space.
		# shows also why wrap_before_characters is important:
		# the "has" would still fit on the line but the following space is too much
		text = " * 13f1c00 -^ (origin/dev) bugfix: subcommand-map has higher-priority than standard-bindings (7 days ago)"
		expected = """\
[22] * 13f1c00 - (origin/d|
[17]             ev)      |
[21]             bugfix:  |
[22]             subcomman|
[19]             d-map    |
[17]             has      |
[20]             higher-  |
[22]             priority |
[18]             than     |
[22]             standard-|
[22]             bindings |
[21]             (7 days  |
[17]             ago)     |"""
		broken_text = self.decorate_text(text, 22, TextLayout.ALIGN_INDENTATION, TextLayout.WRAP_CUSTOM, wrap_before_characters="", wrap_after_characters=" -")
		self.assertEqual(expected, broken_text)

	def test_custom_wrap_before_after(self):
		# similar to test_custom_wrap_after but shows additionally that
		# the line is broken before the space after "has" with wrap_before_characters=" "
		# and that the space at the beginning of the new line is ignored
		text = " * 13f1c00 -^ (origin/dev) bugfix: subcommand-map has higher-priority than standard-bindings (7 days ago)"
		expected = """\
[22] * 13f1c00 - (origin/d|
[17]             ev)      |
[21]             bugfix:  |
[22]             subcomman|
[22]             d-map has|
[20]             higher-  |
[22]             priority |
[18]             than     |
[22]             standard-|
[22]             bindings |
[21]             (7 days  |
[17]             ago)     |"""
		broken_text = self.decorate_text(text, 22, TextLayout.ALIGN_INDENTATION, TextLayout.WRAP_CUSTOM, wrap_before_characters=" ", wrap_after_characters=" -")
		self.assertEqual(expected, broken_text)

	def test_custom_wrap_before(self):
		# test that wrap_before_characters works
		# and that spaces at the beginning of a line are ignored
		# but other characters in wrap_before_characters not
		text = " * 13f1c00 -^ (origin/dev) bugfix: subcommand-map has higher-priority than standard-bindings (7 days ago)"
		expected = """\
[22] * 13f1c00 - (origin/d|
[16]             ev)      |
[20]             bugfix:  |
[22]             subcomman|
[22]             d-map has|
[19]             higher   |
[22]             -priority|
[17]             than     |
[21]             standard |
[22]             -bindings|
[20]             (7 days  |
[17]             ago)     |"""
		broken_text = self.decorate_text(text, 22, TextLayout.ALIGN_INDENTATION, TextLayout.WRAP_CUSTOM, wrap_before_characters=" -", wrap_after_characters="")
		self.assertEqual(expected, broken_text)

	def test_no_auto_move_align_character(self):
		text = "386 +^        auto_move_align_character = True"
		expected = """\
[38]386 +        auto_move_align_character|
[11]     = True                           |"""
		broken_text = self.decorate_text(text, 38, TextLayout.ALIGN_INDENTATION, TextLayout.WRAP_SPACE, auto_move_align_character=False)
		self.assertEqual(expected, broken_text)

	def test_no_auto_move_align_character_long_first_word(self):
		text = "386 +^        auto_move_align_character = True"
		expected = """\
[20]386 +        auto_mo|
[20]     ve_align_charac|
[15]     ter = True     |"""
		broken_text = self.decorate_text(text, 20, TextLayout.ALIGN_INDENTATION, TextLayout.WRAP_SPACE, auto_move_align_character=False)
		self.assertEqual(expected, broken_text)

	def test_long_first_word(self):
		text = "386 +^        auto_move_align_character = True"
		expected = """\
[20]386 +        auto_mo|
[20]             ve_alig|
[20]             n_chara|
[20]             cter = |
[17]             True   |"""
		broken_text = self.decorate_text(text, 20, TextLayout.ALIGN_INDENTATION, TextLayout.WRAP_SPACE)
		self.assertEqual(expected, broken_text)


	# ------- test full width characters -------

	def test_full_width_characters_clip(self):
		text = "これはテストです。日本語を使ってもいいですか？"
		expected = "これはテストです。日"
		broken_text = "\n".join(self.break_text(text, 20, TextLayout.ALIGN_INDENTATION, TextLayout.WRAP_CLIP))
		self.assertEqual(expected, broken_text)

	def test_full_width_characters_ellipsis(self):
		text = "これはテストです。日本語を使ってもいいですか？"
		expected = "これはテストです..."
		broken_text = "\n".join(self.break_text(text, 20, TextLayout.ALIGN_INDENTATION, TextLayout.WRAP_ELLIPSIS, ellipsis_character="..."))
		self.assertEqual(expected, broken_text)

	def test_full_width_characters_wrap_any(self):
		text = "これはテストです。日本語を使ってもいいですか？"
		broken_text = "\n".join(self.break_text(text, 22, TextLayout.ALIGN_INDENTATION, TextLayout.WRAP_ANY))
		expected = """\
これはテストです。日本
語を使ってもいいですか
？"""
		self.assertEqual(expected, broken_text)

	def test_full_width_characters_wrap_space(self):
		text = "* 1234 -^ これはテストです。日本語を使ってもいいですか？ (some days ago)"
		broken_text = "\n".join(self.break_text(text, 22, TextLayout.ALIGN_INDENTATION, TextLayout.WRAP_SPACE))
		expected = '''\
* 1234 - これはテスト
         です。日本語
         を使ってもい
         いですか？ 
         (some days 
         ago)'''
		self.assertEqual(expected, broken_text)

	def test_full_width_characters_bytes(self):
		text = "* 1234 -^ これはテストです。日本語を使ってもいいですか？ (some days ago)".encode('utf8')
		broken_text = b"\n".join(self.break_text(text, 22, TextLayout.ALIGN_INDENTATION, TextLayout.WRAP_SPACE))
		expected = '''\
* 1234 - これはテスト
         です。日本語
         を使ってもい
         いですか？ 
         (some days 
         ago)'''.encode('utf8')
		self.assertEqual(expected, broken_text)

	def test_full_width_characters_too_narrow_window(self):
		text = "* 1234 -^ これはテストです。日本語を使ってもいいですか？ (some days ago)"
		broken_text = self.decorate_text(text, 10, TextLayout.ALIGN_INDENTATION, TextLayout.WRAP_SPACE)
		expected = '''\
[ 9]* 1234 -  |
[10]これはテス|
[10]トです。日|
[10]本語を使っ|
[10]てもいいで|
[ 7]すか？    |
[10](some days|
[ 4]ago)      |'''
		self.assertEqual(expected, broken_text)


	# ------- new line characters -------

	def test_multiline_clip(self):
		text = "item 1) ^First line.\nSecond line. This is somewhat longer than the first.\nAnd look, here is even a third line."
		expected = text.replace("^", "")
		expected = expected[:expected.index('\n')]
		broken_text = "\n".join(self.break_text(text, 22, TextLayout.ALIGN_INDENTATION, TextLayout.WRAP_CLIP))
		self.assertEqual(expected, broken_text)

	def test_multiline_ellipsis_wide_enough(self):
		text = "item 1) ^First line.\nSecond line. This is somewhat longer than the first.\nAnd look, here is even a third line."
		expected = "item 1) First line. ..."
		broken_text = "\n".join(self.break_text(text, 25, TextLayout.ALIGN_INDENTATION, TextLayout.WRAP_ELLIPSIS, ellipsis_character=" ..."))
		self.assertEqual(expected, broken_text)

	def test_multiline_ellipsis_narrow(self):
		text = "item 1) ^First line.\nSecond line. This is somewhat longer than the first.\nAnd look, here is even a third line."
		expected = "item 1) First l..."
		broken_text = "\n".join(self.break_text(text, 18, TextLayout.ALIGN_INDENTATION, TextLayout.WRAP_ELLIPSIS, ellipsis_character="..."))
		self.assertEqual(expected, broken_text)

	def test_multiline_custom_wrap(self):
		text = "long^ish item label)\nFirst line.\nSecond line. This is somewhat longer than the first.\n\nAnd look, here is even a third line."
		expected = """\
[19]longish item label)   |
[15]    First line.       |
[22]    Second line. This |
[22]    is somewhat longer|
[19]    than the first.   |
[ 4]                      |
[22]    And look, here is |
[22]    even a third line.|"""
		broken_text = self.decorate_text(text, 22, TextLayout.ALIGN_INDENTATION, TextLayout.WRAP_CUSTOM, wrap_before_characters=" ", wrap_after_characters=" -")
		self.assertEqual(expected, broken_text)

	def test_multiline_newline_before_align_character(self):
		text = "Please input your data\n>>> ^First line.\nSecond line. This is somewhat longer than the first.\n\nAnd look, here is even a third line."
		expected = """\
[22]Please input your data|
[15]>>> First line.       |
[22]    Second line. This |
[22]    is somewhat longer|
[19]    than the first.   |
[ 4]                      |
[22]    And look, here is |
[22]    even a third line.|"""
		broken_text = self.decorate_text(text, 22, TextLayout.ALIGN_INDENTATION, TextLayout.WRAP_CUSTOM, wrap_before_characters=" ", wrap_after_characters=" -")
		self.assertEqual(expected, broken_text)

	def test_multiline_newline_directly_after_align_character(self):
		text = ">>> ^\nFirst line.\nSecond line. This is somewhat longer than the first.\n\nAnd look, here is even a third line."
		expected = """\
[ 4]>>>                   |
[15]    First line.       |
[22]    Second line. This |
[22]    is somewhat longer|
[19]    than the first.   |
[ 4]                      |
[22]    And look, here is |
[22]    even a third line.|"""
		broken_text = self.decorate_text(text, 22, TextLayout.ALIGN_INDENTATION, TextLayout.WRAP_CUSTOM, wrap_before_characters=" ", wrap_after_characters=" -")
		self.assertEqual(expected, broken_text)

	def test_trailing_newlines(self):
		text = "test\n\n"
		expected = text
		broken_text = "\n".join(self.break_text(text, 22, TextLayout.ALIGN_INDENTATION, TextLayout.WRAP_CUSTOM, wrap_before_characters=" -", wrap_after_characters=""))
		self.assertEqual(expected, broken_text)


	# ------- align character -------

	def test_second_align_charcter_is_printed(self):
		text = "^a^2 + b^2 = c^2"
		expected = text[1:]
		broken_text = "\n".join(self.break_text(text, 22, TextLayout.ALIGN_INDENTATION, TextLayout.WRAP_SPACE, wrap_before_characters=" ", wrap_after_characters=" -"))
		self.assertEqual(expected, broken_text)

	def test_align_left_does_not_gobble_align_character(self):
		text = "a^2 + b^2 = c^2"
		expected = text
		broken_text = "\n".join(self.break_text(text, 22, TextLayout.ALIGN_LEFT, TextLayout.WRAP_SPACE, wrap_before_characters=" ", wrap_after_characters=" -", assert_nonempty=False))
		self.assertEqual(expected, broken_text)


	# ------- test repeat_prefix -------

	def test_repeat_prefix(self):
		text = "    ! ^ERROR\nfailed to execute command"
		expected = """\
[11]    ! ERROR            |
[23]    ! failed to execute|
[13]    ! command          |"""
		broken_text = self.decorate_text(text, 23, TextLayout.ALIGN_INDENTATION, TextLayout.WRAP_SPACE, repeat_prefix=True)
		self.assertEqual(expected, broken_text)

	def test_repeat_split_prefix(self):
		text = "    !^ ERROR\nfailed to execute command"
		expected = """\
[11]    ! ERROR            |
[23]    ! failed to execute|
[13]    ! command          |"""
		broken_text = self.decorate_text(text, 23, TextLayout.ALIGN_INDENTATION, TextLayout.WRAP_SPACE, repeat_prefix=True)
		self.assertEqual(expected, broken_text)

	def test_repeat_split_multi_line_prefix(self):
		text = """\
    ! ------------------
    !^ ERROR\nfailed to execute command
------------------"""
		expected = """\
[24]    ! ------------------|
[11]    ! ERROR             |
[24]    ! failed to execute |
[13]    ! command           |
[24]    ! ------------------|"""
		broken_text = self.decorate_text(text, 24, TextLayout.ALIGN_INDENTATION, TextLayout.WRAP_SPACE, repeat_prefix=True)
		self.assertEqual(expected, broken_text)


	# ------- other tests -------

	def test_empty(self):
		text = ""
		expected = ""
		broken_text = "\n".join(self.break_text(text, 22, TextLayout.ALIGN_INDENTATION, TextLayout.WRAP_CLIP))
		self.assertEqual(expected, broken_text)


	# ------- test copy -------

	def test_copy_same(self):
		layout_original = TextLayout(
			align_character = ".",
			ellipsis_character = "...",
			wrap_after_characters = ") ",
			wrap_before_characters = " (",
			repeat_prefix = True,
			auto_move_align_character = False,
		)
		layout_copy = layout_original.copy()
		self.assertEqual(layout_original.align_character, layout_copy.align_character)
		self.assertEqual(layout_original.ellipsis_character, layout_copy.ellipsis_character)
		self.assertEqual(layout_original.wrap_after_characters, layout_copy.wrap_after_characters)
		self.assertEqual(layout_original.wrap_before_characters, layout_copy.wrap_before_characters)
		self.assertEqual(layout_original.repeat_prefix, layout_copy.repeat_prefix)
		self.assertEqual(layout_original.auto_move_align_character, layout_copy.auto_move_align_character)

	def test_copy_different(self):
		layout_original = TextLayout(
			align_character = ".",
			ellipsis_character = "...",
			wrap_after_characters = ") ",
			wrap_before_characters = " (",
			repeat_prefix = False,
			auto_move_align_character = False,
		)
		layout_copy = layout_original.copy(repeat_prefix=True)
		self.assertEqual(layout_original.align_character, layout_copy.align_character)
		self.assertEqual(layout_original.ellipsis_character, layout_copy.ellipsis_character)
		self.assertEqual(layout_original.wrap_after_characters, layout_copy.wrap_after_characters)
		self.assertEqual(layout_original.wrap_before_characters, layout_copy.wrap_before_characters)
		self.assertEqual(layout_original.repeat_prefix, False)
		self.assertEqual(True, layout_copy.repeat_prefix)
		self.assertEqual(layout_original.auto_move_align_character, layout_copy.auto_move_align_character)


	# ------- utilities -------

	def break_text(self, text, width, align, wrap, **kw):
		assert_nonempty = kw.pop('assert_nonempty', True)
		l = TextLayout("^", **kw)
		layout_struct = l.layout(text, width, align, wrap)
		self.assertTrue(layout_struct, "layout_struct should not be empty")
		if isinstance(text, bytes):
			empty = b""
			space = b" "
			nl = b"\n"
		else:
			empty = ""
			space = " "
			nl = "\n"
		for ln in layout_struct:
			out = empty
			for segment in ln:
				if len(segment) == 2:
					cs, i0 = segment
					segment_text = space * cs
				elif isinstance(segment[2], int):
					cs, i0, i1 = segment
					self.assertGreater(i1, i0)
					segment_text = text[i0:i1]
				else:
					cs, i0, segment_text = segment
					segment_text = segment_text.decode()
				expected_line_width = cs
				if assert_nonempty:
					self.assertGreater(expected_line_width, 0)
				real_line_width = calc_width(segment_text, 0, len(segment_text))
				self.assertEqual(expected_line_width, real_line_width, "segment %r does not have expected width %s" % (segment_text, cs))
				self.assertNotIn(nl, segment_text, "text segment contains newline")

				out += segment_text

			used_line_width = calc_width(out, 0, len(out))
			available_line_width = width
			self.assertLessEqual(used_line_width, available_line_width, "line is too wide\n%r" % out)
			yield out

	def decorate_text(self, text, width, align, wrap, **kw):
		out = []
		for ln in self.break_text(text, width, align, wrap, **kw):
			cs = calc_width(ln, 0, len(ln))
			ln += " " * (width - cs)
			ln += "|"
			ln = "[%2s]%s" % (cs, ln)
			out.append(ln)
		return "\n".join(out)


if __name__ == '__main__':
	unittest.main()
