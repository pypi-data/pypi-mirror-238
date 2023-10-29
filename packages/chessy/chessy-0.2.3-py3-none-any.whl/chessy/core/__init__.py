from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from functools import total_ordering

from chessy import utils


class Color(Enum):
    WHITE = auto()
    BLACK = auto()

    def invert(self) -> Color:
        match self:
            case Color.WHITE:
                return Color.BLACK
            case Color.BLACK:
                return Color.WHITE


class Type(Enum):
    PAWN = auto()
    KNIGHT = auto()
    BISHOP = auto()
    ROOK = auto()
    QUEEN = auto()
    KING = auto()


@dataclass(frozen=True, slots=True)
class Piece:
    ptype: Type
    color: Color

    @staticmethod
    def from_letter(letter: str) -> Piece:
        """
        Create a Piece from a given letter code.

        ValueError is raised if letter is not an allowed letter.
        """

        if letter.lower() not in {"p", "k", "q", "r", "n", "b"}:
            raise ValueError(f"Cannot convert {letter} to a piece")

        t: Type
        match letter.lower():
            case "p":
                t = Type.PAWN
            case "k":
                t = Type.KING
            case "q":
                t = Type.QUEEN
            case "r":
                t = Type.ROOK
            case "n":
                t = Type.KNIGHT
            case "b":
                t = Type.BISHOP
            case _:
                utils.unreachable()

        return Piece(ptype=t, color=Color.WHITE if letter.isupper() else Color.BLACK)

    def to_letter(self) -> str:
        """Convert the current Piece into a letter code."""

        ret: str
        match self.ptype:
            case Type.PAWN:
                ret = "p"
            case Type.KING:
                ret = "k"
            case Type.QUEEN:
                ret = "q"
            case Type.ROOK:
                ret = "r"
            case Type.KNIGHT:
                ret = "n"
            case Type.BISHOP:
                ret = "b"

        return ret.upper() if self.color.value == Color.WHITE.value else ret.lower()

    def direction_factor(self) -> int:
        """
        If the current piece is a pawn, return its direction factor:
        1 for white, -1 for black.

        If the current piece is non-pawn, raise ValueError.
        """

        if self.ptype != Type.PAWN:
            raise ValueError("Non-pawn pieces do not have a defined direction_factor")

        return 1 if self.color == Color.WHITE else -1


@total_ordering
class Square(Enum):
    a1 = 0  # To make sure we can index Board through squares.
    b1 = auto()
    c1 = auto()
    d1 = auto()
    e1 = auto()
    f1 = auto()
    g1 = auto()
    h1 = auto()

    a2 = auto()
    b2 = auto()
    c2 = auto()
    d2 = auto()
    e2 = auto()
    f2 = auto()
    g2 = auto()
    h2 = auto()

    a3 = auto()
    b3 = auto()
    c3 = auto()
    d3 = auto()
    e3 = auto()
    f3 = auto()
    g3 = auto()
    h3 = auto()

    a4 = auto()
    b4 = auto()
    c4 = auto()
    d4 = auto()
    e4 = auto()
    f4 = auto()
    g4 = auto()
    h4 = auto()

    a5 = auto()
    b5 = auto()
    c5 = auto()
    d5 = auto()
    e5 = auto()
    f5 = auto()
    g5 = auto()
    h5 = auto()

    a6 = auto()
    b6 = auto()
    c6 = auto()
    d6 = auto()
    e6 = auto()
    f6 = auto()
    g6 = auto()
    h6 = auto()

    a7 = auto()
    b7 = auto()
    c7 = auto()
    d7 = auto()
    e7 = auto()
    f7 = auto()
    g7 = auto()
    h7 = auto()

    a8 = auto()
    b8 = auto()
    c8 = auto()
    d8 = auto()
    e8 = auto()
    f8 = auto()
    g8 = auto()
    h8 = auto()

    def rank(self) -> int:
        """Get the rank, from 0 to 7. Ranks are horizontal rows."""
        return self.value // 8

    def file(self) -> int:
        """Get the file, from 0 to 7. Files are vertical rows."""
        return self.value % 8

    @classmethod
    def last_file(cls) -> int:
        return cls.h7.file()

    @classmethod
    def first_rank(cls) -> int:
        return cls.h1.rank()

    @classmethod
    def last_rank(cls) -> int:
        return cls.h8.rank()

    def __lt__(self, other: Square) -> bool:
        return self.value < other.value


@dataclass(slots=True)
class CastlingAvailability:
    white_kingside: bool
    white_queenside: bool
    black_kingside: bool
    black_queenside: bool

    def disable_for_color(self, color: Color) -> None:
        if color == Color.WHITE:
            self.white_kingside = False
            self.white_queenside = False
        else:
            self.black_kingside = False
            self.black_queenside = False

    def disable_for_square(self, square: Square) -> None:
        if square == Square.a1:
            self.white_queenside = False
        elif square == Square.h1:
            self.white_kingside = False
        elif square == Square.a8:
            self.black_queenside = False
        elif square == Square.h8:
            self.black_kingside = False


@dataclass(frozen=True, slots=True)
class Move:
    source: Square
    target: Square
    promotion: Type | None = None

    def __post_init__(self) -> None:
        if self.promotion is not None:
            target_rank = self.target.rank()

            assert target_rank in {Square.first_rank(), Square.last_rank()}
            assert self.promotion not in {Type.KING, Type.PAWN}

    @staticmethod
    def from_long_algebraic_notation(value: str) -> Move:
        """
        Attempt to build a Move given a value in long algebraic notation.

        Raise ValueError if the value is not well-formed.
        """

        min_long_algebraic_notation_size = 4
        if len(value) < min_long_algebraic_notation_size:
            raise ValueError(f"{value} is too short to be a long algebraic notation")

        max_long_algebraic_notation_size = 5
        if len(value) > max_long_algebraic_notation_size:
            raise ValueError(f"{value} is too long to be a long algebraic notation")

        try:
            sq1 = Square[value[:2]]
            if len(value) == max_long_algebraic_notation_size:
                sq2 = Square[value[2:-1]]
                p = value[-1]
            else:
                sq2 = Square[value[2:]]
                p = None
        except KeyError:
            raise ValueError(
                f"{value} does not represent two squares properly"
            ) from None

        if p is not None and p.lower() in {"k", "p"}:
            raise ValueError("Cannot promote to king or pawn")

        try:
            ptype = Piece.from_letter(p).ptype if p is not None else None
        except ValueError as e:
            raise e from e

        return Move(sq1, sq2, ptype)

    def to_long_algebraic_notation(self) -> str:
        source = self.source
        target = self.target
        promotion = self.promotion

        move = f"{source.name}{target.name}"
        if promotion is not None:
            # Black pieces have a lowercase code, which in this case is what we want
            # (even for white pieces).
            piece = Piece.to_letter(Piece(promotion, Color.BLACK))
            move += piece

        return move
