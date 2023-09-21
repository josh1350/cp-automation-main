# flake8: noqa
import re
from datetime import datetime

from src.helpers.date_helper import DateHelper
from src.models.documents.mailings_row_model import MailingsRowModel
from src.models.documents.reports_row_model import ReportsRowModel
from src.models.documents.statements_row_model import StatementsRowModel
from src.models.documents.taxes_row_model import TaxesRowModel


class DocumentsApiModel:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.date = kwargs.get("date")
        self.day = re.sub(r",\s\d{4}$", "", self.date)
        self.year = datetime.strptime(self.date, "%b %d, %Y").year
        self.account_number = kwargs.get("accountNumber")
        self.account_name = kwargs.get("accountName")
        self.registration_type = kwargs.get("registrationType")
        self.type = kwargs.get("type")
        self.object_id = kwargs.get("objectId")
        self.virtual_table = kwargs.get("virtualTable")
        self.time_taken = kwargs.get("timeTaken")
        self.related_accounts = [RelatedAccount(**data) for data in kwargs.get("relatedAccounts")]

    def get_formatted_account_name(self):
        account_name = " ".join(self.account_name.split())
        return f"{account_name}\n{self.account_number} • {self.registration_type}"

    def get_statements_format(self):
        return StatementsRowModel(self.day, self.year, self.get_formatted_account_name(), self.name)

    def get_mailing_format(self):
        return MailingsRowModel(self.day, self.year, self.get_formatted_account_name(), self.name)

    def get_tax_format(self):
        year = f"Tax Year {self.year}"
        return TaxesRowModel(self.name, year, self.get_formatted_account_name())

    def get_report_format(self):
        if len(self.related_accounts) > 3:
            account_names = "\n".join(
                [related_account.account_name.replace("  ", " ") for related_account in self.related_accounts[:3]]
            )
            additional_accounts = len(self.related_accounts) - 3
            formatted_string = f"{account_names}\nShow {additional_accounts} more account(s)"
        else:
            formatted_string = "\n".join([related_account.account_name for related_account in self.related_accounts])

        return ReportsRowModel(
            DateHelper.get_quarter(self.day), self.year, formatted_string.strip(), "Quaterly Performance Report"
        )


class RelatedAccount:
    def __init__(self, **kwargs):
        self.account_number = kwargs.get("accountNumber")
        self.account_name = kwargs.get("accountName")
        self.registration_type = kwargs.get("registrationType")
