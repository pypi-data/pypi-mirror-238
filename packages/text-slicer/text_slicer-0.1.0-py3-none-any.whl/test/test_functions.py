# text_toolkit/tests/test_functions.py
import pytest
from text_toolkit import clean_text, split_sentences, slice_by_sentence

def test_clean_text():
    text = "<p>Hello, world! 你好，世界！</p>"
    expected_output = "Hello, world! 你好，世界！"
    assert clean_text(text) == expected_output

def test_split_sentences():
    text = "他说：“早上好！今天的天气非常宜人。”"
    expected_output = ['他说：“早上好！今天的天气非常宜人。”']
    assert split_sentences(text) == expected_output

def test_slice_by_sentence():
    text = "他说：“早上好！今天的天气非常宜人。”"
    expected_output = ['他说：“早上好！今天的天气非常宜人。”']
    assert slice_by_sentence(text, chunk_size=30) == expected_output
