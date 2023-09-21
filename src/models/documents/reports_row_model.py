# flake8: noqa


class ReportsRowModel:
    def __init__(self, quarter, year, account, name):
        self.quarter = quarter
        self.year = year
        self.account = account
        self.name = name

    def __eq__(self, other):
        if not isinstance(other, ReportsRowModel):
            return False
        if (
            self.quarter != other.quarter
            and self.year != other.year
            and self.name != other.name
            and self.account != other.account
        ):
            return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)
