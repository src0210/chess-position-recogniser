import chess
import chess.engine
from dataclasses import dataclass

STOCKFISH_PATH = "/opt/homebrew/bin/stockfish"


def get_best_move(fen: str, time_limit: float = 2.0, depth_limit: int = 20) -> str:
    """Return Stockfish's best move for a FEN, in UCI notation (e.g. 'e2e4')."""
    board = chess.Board(fen)
    with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
        result = engine.play(board, chess.engine.Limit(time=time_limit, depth=depth_limit))
    return result.move.uci()


@dataclass
class Analysis:
    best_move: str          # UCI, e.g. "e2e4"
    centipawns: int | None  # White's advantage in 1/100 pawn; None if mate found
    mate_in: int | None     # +N = White mates in N, -N = Black mates in N; else None


def analyse_position(fen: str, time_limit: float = 0.1, depth: int | None = None) -> Analysis:
    board = chess.Board(fen)
    limit = chess.engine.Limit(time=time_limit, depth=depth)
    with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
        info = engine.analyse(board, limit)

    score = info["score"].white()
    return Analysis(
        best_move=info["pv"][0].uci(),
        centipawns=score.score(),
        mate_in=score.mate(),
    )