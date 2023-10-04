import pytest
from gl2f.core import board

def test_active_boards():
	keys = {i['key'] for i in  board.table()}
	assert set(board.active()).issubset(keys)
