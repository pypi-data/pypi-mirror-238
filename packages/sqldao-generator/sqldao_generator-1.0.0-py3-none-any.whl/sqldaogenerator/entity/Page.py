from dataclasses import dataclass


@dataclass
class Page:
    order_by = None
    page_no: int = None
    page_size: int = None
