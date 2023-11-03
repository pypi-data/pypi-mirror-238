from dataclasses import dataclass, asdict


@dataclass
class General:
    id: int = None
    id_in: list[int] = None
    id_gte: int = None
    id_lte: int = None

    def __getitem__(self, field):
        return asdict(self)[field]
