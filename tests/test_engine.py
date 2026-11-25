import chess
import pytest
from src.engine import StockfishEngine, get_best_move

START_FEN = chess.STARTING_FEN

# White to move, Qxf7# is mate
WHITE_MATE_FEN = "r1bqkbnr/pppp1ppp/2n5/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR w KQkq - 2 3"
# Black to move, Qh4# is mate (Fool's Mate)
BLACK_MATE_FEN = "rnbqkbnr/pppp1ppp/8/4p3/6P1/5P2/PPPPP2P/RNBQKBNR b KQkq - 0 2"
# Start position with Black's queen removed: White is clearly better
WHITE_UP_QUEEN_FEN = "rnb1kbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


@pytest.fixture(scope="module")
def engine():
    with StockfishEngine() as eng:
        yield eng


def test_returns_legal_move():
    move = get_best_move(START_FEN)
    board = chess.Board(START_FEN)
    assert chess.Move.from_uci(move) in board.legal_moves


def test_get_best_move_invalid_fen_raises():
    with pytest.raises(ValueError):
        get_best_move("not a fen")


def test_analyse_invalid_fen_raises(engine):
    with pytest.raises(ValueError):
        engine.analyse("not a fen")


def test_start_position_is_roughly_equal(engine):
    result = engine.analyse(START_FEN, depth=12)
    assert result.mate_in is None
    assert abs(result.centipawns) < 100  # within a pawn


def test_white_up_a_queen_is_positive(engine):
    result = engine.analyse(WHITE_UP_QUEEN_FEN, depth=12)
    assert result.centipawns > 300  # roughly a piece or more ahead


def test_white_mate_in_one(engine):
    result = engine.analyse(WHITE_MATE_FEN, depth=12)
    assert result.mate_in == 1
    assert result.best_move == "h5f7"


def test_black_mate_in_one_is_negative(engine):
    result = engine.analyse(BLACK_MATE_FEN, depth=12)
    assert result.mate_in == -1
    assert result.best_move == "d8h4"