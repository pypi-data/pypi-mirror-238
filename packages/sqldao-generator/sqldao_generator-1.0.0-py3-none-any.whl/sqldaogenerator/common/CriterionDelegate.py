from dataclasses import dataclass
from typing import Any

import sqlalchemy
from sqlalchemy import func, Column, cast

from sqldaogenerator.common.Criterion import Criterion


@dataclass
class CriterionDelegate:
    _criterion: Any

    def end(self) -> Criterion:
        return self._criterion.build()

    def _build_column(self, column: Column, group=False, count=False, max=False, min=False, sum=False):
        self._labels.append(column.name)
        if count:
            self._counts.append(func.count(column))
        elif max:
            self._maxes.append(func.max(column))
        elif min:
            self._mines.append(func.min(column))
        elif sum:
            if column.type.python_type == int:
                self._sums.append(cast(func.sum(column), sqlalchemy.Integer))
            else:
                self._sums.append(func.sum(column))
        else:
            if group:
                self._groups.append(column)
            self._columns.append(column)
        return self

    def _build_equal(self, column: Column, value, reverse=False):
        if value is not None:
            if reverse:
                self._filters.append(column != value)
            else:
                self._filters.append(column == value)
        return self

    def _build_in(self, column: Column, value: list = None, reverse=False):
        if value:
            if reverse:
                self._filters.append(column.notin_(value))
            else:
                self._filters.append(column.in_(value))
        return self

    def _build_like(self, column: Column, value: str, reverse=False, left="%", right="%"):
        if value:
            if reverse:
                self._filters.append(column.not_like(f"{left}{value}{right}"))
            else:
                self._filters.append(column.like(f"{left}{value}{right}"))
        return self

    def _build_null(self, column: Column, reverse=False):
        if reverse:
            self._filters.append(column.isnot(None))
        else:
            self._filters.append(column.is_(None))
        return self

    def _build_gte(self, column: Column, value):
        if value:
            self._filters.append(column >= value)
        return self

    def _build_lte(self, column: Column, value):
        if value:
            self._filters.append(column <= value)
        return self

    def _build_modify(self, column: Column, value):
        self._values[column.name] = value
        return self
