from pprog import identity, AttrCaller, ConstantCreator, perm, PermArgsExecutor


def test_identity():
    result = identity(3, "hello", key="value")
    assert result == 3


def test_AttrCaller():
    caller = AttrCaller("upper")
    result = caller("test")
    assert result == "TEST"


def test_ConstantCreator():
    creator = ConstantCreator(4)
    result = creator()
    assert result == 4


def test_perm():
    result = perm(["a", "b", "c", "d", "e", "f", "g"], [1, 2, 4])
    assert result == ["a", "c", "e", "d", "b", "f", "g"]


def test_PermArgsExecutor():
    executor = PermArgsExecutor(range)
    result = executor(4, 2)
    assert result == range(2, 4)
