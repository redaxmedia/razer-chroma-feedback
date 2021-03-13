from chroma_feedback import helper


def test_to_lower_case() -> None:
	assert helper.to_lower_case(None) == 'none'
	assert helper.to_lower_case('SUCCESS') == 'success'


def test_has_argument() -> None:
	assert helper.has_argument('invalid') == False


def test_is_linux() -> None:
	assert type(helper.is_linux()) == bool


def test_get_first() -> None:
	assert helper.get_first(
	[
		1,
		2,
		3
	]) == 1


def test_get_last() -> None:
	assert helper.get_last(
	[
		1,
		2,
		3
	]) == 3
