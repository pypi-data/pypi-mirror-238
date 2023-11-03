from dataclasses import dataclass, field

from sqldaogenerator.generator.enums.MySqlTypeEnum import MySqlTypeEnum


@dataclass
class ColumnTemplate:
    entity_name: str = None
    column_name: str = None
    column_type: str = None
    alchemy_type: str = None
    py_type: str = None
    column_properties: list[str] = field(default_factory=list)

    def column(self, name: str, column_type: str):
        self.column_name = name
        self.column_type = column_type
        self.alchemy_type = MySqlTypeEnum[column_type].value[0]
        self.py_type = next(x.value[1] for x in MySqlTypeEnum.__members__.values() if column_type in x.name)
        self.column_properties.append(self.alchemy_type)
        return self

    def autoincrement(self):
        self.column_properties.append('autoincrement=True')
        return self

    def primary_key(self):
        self.column_properties.append('primary_key=True')
        return self

    def comment(self, comment: str):
        self.column_properties.append(f"comment='{comment}'")
        return self

    @classmethod
    def builder(cls, entity_name: str):
        instance = cls()
        instance.entity_name = entity_name
        return instance

    def build_alchemy_column(self):
        return f"{self.column_name} = Column({', '.join(self.column_properties)})"

    def build_column(self):
        return f"""def {self.column_name}(self, group=False, count=False, max=False, min=False, sum=False):
        return self._build_column({self.entity_name}.{self.column_name}, group, count, max, min, sum)"""

    def build_modify(self):
        return f"""def {self.column_name}(self, value: {self.py_type}):
        return self._build_modify({self.entity_name}.{self.column_name}, value)"""

    def build_equal(self):
        return f"""def {self.column_name}(self, value: {self.py_type} = None, reverse=False):
        return self._build_equal({self.entity_name}.{self.column_name}, value, reverse)"""

    def build_in(self):
        return f"""def {self.column_name}_in(self, value: list[{self.py_type}] = None, reverse=False):
        return self._build_in({self.entity_name}.{self.column_name}, value, reverse)"""

    def build_like(self):
        return f"""def {self.column_name}_like(self, value: {self.py_type} = None, reverse=False, left="%", right="%"):
        return self._build_like({self.entity_name}.{self.column_name}, value, reverse, left, right)"""

    def build_null(self):
        return f"""def {self.column_name}_null(self, reverse=False):
        return self._build_null({self.entity_name}.{self.column_name}, reverse)"""

    def build_num_compare(self):
        return f"""def {self.column_name}_gte(self, value: {self.py_type} = None):
        return self._build_gte({self.entity_name}.{self.column_name}, value)

    def {self.column_name}_lte(self, value: {self.py_type} = None):
        return self._build_lte({self.entity_name}.{self.column_name}, value)"""

    def build_datetime_compare(self):
        return f"""def {self.column_name}_start(self, value: {self.py_type} = None):
        return self._build_gte({self.entity_name}.{self.column_name}, value)

    def {self.column_name}_end(self, value: {self.py_type} = None):
        return self._build_lte({self.entity_name}.{self.column_name}, value)"""
