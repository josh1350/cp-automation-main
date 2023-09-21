# flake8: noqa
from src.models.documents.row_model import RowModel


class TaxesRowModel(RowModel):
    def __init__(self, name, year, account):
        super().__init__(account, name, year)

    def __eq__(self, other):
        if not isinstance(other, TaxesRowModel):
            return False
        if self.year != other.year and self.account != other.account and self.name != other.name:
            return False
        return True
