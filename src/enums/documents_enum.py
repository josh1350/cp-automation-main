from enum import Enum


class FilterType(Enum):
    DATE = "date"
    TAX_YEAR = "tax year"
    ACCOUNTS = "accounts"
    TYPE = "type"


class DocumentsTab(Enum):
    STATEMENTS = "statements"
    REPORTS = "reports"
    MAILINGS = "mailings"
    TAXES = "taxes"
