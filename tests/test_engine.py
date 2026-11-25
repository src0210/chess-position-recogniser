import chess
import pytest
from src.engine import get_best_move
from src.engine import analyse_position
from src.engine import StockfishEngine

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


def test_start_position_is_roughly_equal():
    result = analyse_position(START_FEN, depth=12)
    assert result.mate_in is None
    assert abs(result.centipawns) < 100   # within a pawn


def test_mate_in_one_reports_mate():
    fen = "r1bqkbnr/pppp1ppp/2n5/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR w KQkq - 2 3"
    result = analyse_position(fen, depth=12)
    assert result.mate_in == 1
    assert result.best_move == "h5f7"

def test_black_mate_in_one_is_negative():
    # Black to move, Qh4# is mate
    fen = "rnbqkbnr/pppp1ppp/8/4p3/6P1/5P2/PPPPP2P/RNBQKBNR b KQkq - 0 2"
    result = analyse_position(fen, depth=12)
    assert result.best_move == "d8h4"
    assert result.mate_in == -1

@pytest.fixture(scope="module")
def engine():
    with StockfishEngine() as eng:
        yield eng


def test_start_position_with_fixture(engine):
    result = engine.analyse(START_FEN, depth=12)
    assert abs(result.centipawns) < 100