class RowModel:
    def __init__(self, account, name, year):
        self.account = account
        self.name = name
        self.year = year

    def get_account_filter_format(self):
        parts = self.account.split("\n")

        account_number = parts[1].split(" • ")[0]
        account_name = parts[0]
        registration_type = parts[1].split(" • ")[1]
        return f"{account_number}-{account_name}-{registration_type}"

    def __ne__(self, other):
        return not self.__eq__(other)
