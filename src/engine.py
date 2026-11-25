import chess
import chess.engine

STOCKFISH_PATH = "/opt/homebrew/bin/stockfish"


def get_best_move(fen: str, time_limit: float = 0.1) -> str:
    """Return Stockfish's best move for a FEN, in UCI notation (e.g. 'e2e4')."""
    board = chess.Board(fen)
    with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
        result = engine.play(board, chess.engine.Limit(time=time_limit))
    return result.move.uci()