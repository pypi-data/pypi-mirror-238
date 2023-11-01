from pyjt import FrameFinder, ElementNotFoundError

from tools import assert_raises


def test_dispose_frame(hwlocal):
    assert hwlocal is not None
    hwlocal.dispose()
    assert_raises(ElementNotFoundError, lambda: FrameFinder.find(title="hwlocal"))


def test_close_frame(hwlocal):
    assert hwlocal is not None
    hwlocal.close()
    assert_raises(ElementNotFoundError, lambda: FrameFinder.find(title="hwlocal"))
