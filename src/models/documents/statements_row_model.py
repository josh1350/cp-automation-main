# flake8: noqa
from src.models.documents.row_model import RowModel


class StatementsRowModel(RowModel):
    def __init__(self, date, year, account, name):
        super().__init__(account, name, year)
        self.date = f"{date}, {year}"

    def __eq__(self, other):
        if not isinstance(other, StatementsRowModel):
            return False
        if (
            self.date != other.date
            and self.year != other.year
            and self.account != other.account
            and self.name != other.name
        ):
            return False
        return True
