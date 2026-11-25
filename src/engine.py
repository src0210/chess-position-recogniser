from dataclasses import dataclass

import chess
import chess.engine

STOCKFISH_PATH = "/opt/homebrew/bin/stockfish"


@dataclass(frozen=True)
class Analysis:
    best_move: str  # UCI, e.g. "e2e4"
    centipawns: int | None  # White's advantage in 1/100 pawn; None if mate found
    mate_in: int | None  # +N = White mates in N, -N = Black mates in N; else None


class StockfishEngine:
    """One Stockfish process, reused across calls. Use as a context manager."""

    def __init__(self, path: str = STOCKFISH_PATH):
        self._engine = chess.engine.SimpleEngine.popen_uci(path)

    def analyse(
        self, fen: str, time_limit: float = 0.1, depth: int | None = None
    ) -> Analysis:
        """Analyse a position. Raises ValueError for a bad FEN or a finished game."""
        board = chess.Board(fen)
        if board.is_game_over():
            raise ValueError(f"Game is already over, no best move: {fen}")

        limit = chess.engine.Limit(time=time_limit, depth=depth)
        info = self._engine.analyse(board, limit)

        score = info["score"].white()
        return Analysis(
            best_move=info["pv"][0].uci(),
            centipawns=score.score(),
            mate_in=score.mate(),
        )

    def close(self) -> None:
        self._engine.quit()

    def __enter__(self) -> "StockfishEngine":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()


def analyse_position(
    fen: str, time_limit: float = 0.1, depth: int | None = None
) -> Analysis:
    """One-off analysis (starts and stops its own engine)."""
    with StockfishEngine() as engine:
        return engine.analyse(fen, time_limit, depth)


def get_best_move(fen: str, time_limit: float = 2.0, depth: int | None = 20) -> str:
    """Return Stockfish's best move for a FEN, in UCI notation (e.g. 'e2e4')."""
    return analyse_position(fen, time_limit, depth).best_move
