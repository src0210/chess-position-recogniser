import chess
import pytest
from src.engine import get_best_move

START_FEN = chess.STARTING_FEN


def test_returns_legal_move():
    move = get_best_move(START_FEN)
    board = chess.Board(START_FEN)
    assert chess.Move.from_uci(move) in board.legal_moves


def test_finds_mate_in_one():
    # White to move; Qh5 is not it, but Qxf7# is
    fen = "r1bqkbnr/pppp1ppp/2n5/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR w KQkq - 2 3"
    assert get_best_move(fen) == "h5f7"


def test_invalid_fen_raises():
    with pytest.raises(ValueError):
        get_best_move("not a fen")