from __future__ import annotations
from enum import Enum

from functools import lru_cache
from typing import List, overload

from pydantic import BaseModel, ConfigDict, RootModel

from deciphon_snap.amino import AminoInterval
from deciphon_snap.interval import PyInterval

__all__ = ["Match", "MatchList", "LazyMatchList", "MatchListInterval", "MatchElemName"]


class MatchElemName(Enum):
    QUERY = 1
    STATE = 2
    CODON = 3
    AMINO = 4


class Match(BaseModel):
    query: str
    state: str
    codon: str
    amino: str
    _position: int | None = None

    @classmethod
    def from_string(cls, x: str):
        y = x.split(",", 3)
        return cls(query=y[0], state=y[1], codon=y[2], amino=y[3])

    @property
    def position(self):
        assert self._position is not None
        return self._position

    @position.setter
    def position(self, x: int):
        self._position = x

    def __str__(self):
        query = self.query if len(self.query) > 0 else "∅"
        state = self.state
        codon = self.codon if len(self.codon) > 0 else "∅"
        amino = self.amino if len(self.amino) > 0 else "∅"
        return f"({query},{state},{codon},{amino})"


class MatchList(RootModel):
    root: List[Match]

    @classmethod
    def from_string(cls, x: str):
        return cls.model_validate([Match.from_string(i) for i in x.split(";")])

    def __len__(self):
        return len(self.root)

    @overload
    def __getitem__(self, i: int) -> Match:
        ...

    @overload
    def __getitem__(self, i: slice) -> MatchList:
        ...

    def __getitem__(self, i: int | slice):
        if isinstance(i, slice):
            return MatchList.model_validate(self.root[i])
        match = self.root[i]
        assert isinstance(match, Match)
        return match

    def __iter__(self):
        return iter(self.root)

    def __str__(self):
        return " ".join(str(i) for i in self.root)

    @property
    def query(self):
        return "".join(x.query for x in iter(self))

    @property
    def state(self):
        return "".join(x.state for x in iter(self))

    @property
    def codon(self):
        return "".join(x.codon for x in iter(self))

    @property
    def amino(self):
        return "".join(x.amino for x in iter(self))


class MatchListInterval(PyInterval):
    ...


class MatchListIntervalBuilder:
    def __init__(self, match_list: MatchList):
        self._amino_map = [i for i, x in enumerate(match_list) if len(x.amino) > 0]

    def make_from_amino_interval(
        self, amino_interval: AminoInterval
    ) -> MatchListInterval:
        i = amino_interval
        x = self._amino_map[i.slice]
        return MatchListInterval(start=x[0], stop=x[-1] + 1)


class LazyMatchList(BaseModel):
    raw: str
    model_config = ConfigDict(frozen=True)

    @lru_cache(maxsize=1)
    def evaluate(self):
        return MatchList.from_string(self.raw)

    def __len__(self):
        return len(self.evaluate())

    def __getitem__(self, i):
        return self.evaluate()[i]

    def __iter__(self):
        return iter(self.evaluate())

    def __str__(self):
        return str(self.evaluate())

    def __repr__(self):
        return repr(self.evaluate())

    @property
    def query(self):
        return self.evaluate().query

    @property
    def state(self):
        return self.evaluate().state

    @property
    def codon(self):
        return self.evaluate().codon

    @property
    def amino(self):
        return self.evaluate().amino
