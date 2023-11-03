from dataclasses import dataclass, field

from sqlalchemy import BinaryExpression, Column

from sqldaogenerator.entity.Page import Page


@dataclass
class Criterion:
    labels: list[str] = field(default_factory=list)
    columns: list[Column] = field(default_factory=list)
    groups: list[Column] = field(default_factory=list)
    counts: list = field(default_factory=list)
    maxes: list = field(default_factory=list)
    mines: list = field(default_factory=list)
    sums: list = field(default_factory=list)
    page: Page = field(default_factory=Page)
    filters: list[BinaryExpression] = field(default_factory=list)
    values: dict[str, any] = field(default_factory=dict)
    distinct: bool = False

    def __getitem__(self, item):
        return self.values[item]

    def get(self, key, default):
        return self.values.get(key, default)

    def items(self):
        return self.values.items()
