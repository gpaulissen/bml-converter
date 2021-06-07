from utils import about


def test_about():
    expected = {'__title__', '__author__', '__email__', '__version_info__', '__version__', '__license__', '__copyright__', '__url__', '__help_url__'}
    actual = set(dir(about))
    assert actual.issuperset(expected), f'The actual names of the about module are {actual} but expected are {expected}'


if __name__ == '__main__':
    test_about()
