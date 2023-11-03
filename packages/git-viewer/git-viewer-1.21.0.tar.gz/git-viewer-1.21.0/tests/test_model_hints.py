#!../venv/bin/pytest

from git_viewer.model_hints import generate_keys


def test__generate_keys__2_1() -> None:
	assert list(generate_keys('ab', 1)) == ['a']

def test__generate_keys__2_2() -> None:
	assert list(generate_keys('ab', 2)) == ['a', 'b']

def test__generate_keys__2_3() -> None:
	assert list(generate_keys('ab', 3)) == ['a', 'ba', 'bb']

def test__generate_keys__2_4() -> None:
	assert list(generate_keys('ab', 4)) == ['aa', 'ab', 'ba', 'bb']

def test__generate_keys__2_5() -> None:
	assert list(generate_keys('ab', 5)) == ['aa', 'ab', 'ba', 'bba', 'bbb']

def test__generate_keys__2_6() -> None:
	assert list(generate_keys('ab', 6)) == ['aa', 'ab', 'baa', 'bab', 'bba', 'bbb']

def test__generate_keys__2_16() -> None:
	assert list(generate_keys('ab', 16)) == [i+j+k+l for i in 'ab' for j in 'ab' for k in 'ab' for l in 'ab']



def test__generate_keys__4_1() -> None:
	assert list(generate_keys('fjgh', 1)) == ['f']

def test__generate_keys__4_4() -> None:
	assert list(generate_keys('fjgh', 4)) == ['f', 'j', 'g', 'h']

def test__generate_keys__4_5() -> None:
	assert list(generate_keys('fjgh', 5)) == ['f', 'j', 'g', 'hf', 'hj']

def test__generate_keys__4_7() -> None:
	assert list(generate_keys('fjgh', 7)) == ['f', 'j', 'g', 'hf', 'hj', 'hg', 'hh']

def test__generate_keys__4_8() -> None:
	assert list(generate_keys('fjgh', 8)) == ['f', 'j', 'gf', 'gj', 'gg', 'gh', 'hf', 'hj']



def test__many() -> None:
	for i in range(1, 100):
		keys = list(generate_keys('fjgh', i))
		assert len(keys) == i
		assert len(set(keys)) == i
