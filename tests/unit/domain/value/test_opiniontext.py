import pytest
from domain.model.value.OpinionText import OpinionText

def test_opiniontext_valid():
    txt = "A valid opinion"
    op = OpinionText(txt)
    assert op.value == txt

def test_opiniontext_empty():
    with pytest.raises(ValueError):
        OpinionText("")

def test_opiniontext_too_long():
    with pytest.raises(ValueError):
        OpinionText("x" * 1001)  # assuming max length 1000

