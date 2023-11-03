from dataclasses import dataclass
from types import ModuleType


@dataclass
class EntityCreateReq:
    entity_package: ModuleType | str
    entity_name: str
    table: str
    dao_package: ModuleType | str
