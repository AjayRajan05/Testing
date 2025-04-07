from calc import add
import pytest

def test_add():
    assert add(1,2) == 3
    assert add(-1,1) == 0
    assert add(0,0) == 0

def test_raises_integer_plus_string():
    with pytest.raises(TypeError):
        add(1,'a')