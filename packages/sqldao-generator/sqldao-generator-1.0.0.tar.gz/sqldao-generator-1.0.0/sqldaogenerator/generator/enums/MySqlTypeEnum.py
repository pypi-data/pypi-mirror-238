from enum import Enum


# from sqlalchemy import BigInteger, VARCHAR, CHAR, Text, SmallInteger, Integer, Double, DateTime, JSON, TIMESTAMP


class MySqlTypeEnum(Enum):
    bigint = ('BigInteger', 'int')
    varchar = ('VARCHAR', 'str')
    char = ('CHAR', 'str')
    text = ('Text', 'str')
    tinyint = ('SmallInteger', 'int')
    int = ('Integer', 'int')
    double = ('Double', 'float')
    datetime = ('DateTime', 'datetime | str')
    timestamp = ('TIMESTAMP', 'datetime | str')
    json = ('JSON', 'str')

    @classmethod
    def is_string(cls, name: str):
        return name in [cls.varchar.name, cls.char.name, cls.text.name, cls.json.name]

    @classmethod
    def is_number(cls, name: str):
        return name in [cls.tinyint.name, cls.int.name, cls.double.name, cls.bigint.name]

    @classmethod
    def is_date(cls, name: str):
        return name in [cls.datetime.name, cls.timestamp.name]
