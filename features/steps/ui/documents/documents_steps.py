import re

from behave import then, when

from src.enums.documents_enum import DocumentsTab, FilterType
from src.helpers.assertions import Assert
from src.helpers.behave_helper import BehaveHelper
from src.helpers.date_helper import DateHelper
from src.helpers.exceptions.automation_exception import AutomationException
from src.helpers.logger import Log
from src.helpers.string_helper import StringHelper
from src.models.documents.documents_api_model import DocumentsApiModel
from src.models.documents.mailings_row_model import MailingsRowModel
from src.models.documents.reports_row_model import ReportsRowModel
from src.models.documents.statements_row_model import StatementsRowModel
from src.models.documents.taxes_row_model import TaxesRowModel
from src.ui.components.documens.report_tab_component import ReportsTab
from src.ui.pages.dashboard.dashboard_page import DashboardPage
from src.ui.pages.documents.documents_page import DocumentsPage
from src.ui.pages.documents.documents_preview_page import DocumentsPreviewPage

log = Log().logger


@when('I open "{tab}" tab on Documents Page')
def navigate_to_documents_tab(context, tab):
    tab = DocumentsTab(tab.lower())
    tab_mapping = {
        DocumentsTab.STATEMENTS: DocumentsPage(context).open_statements_tab,
        DocumentsTab.REPORTS: DocumentsPage(context).open_reports_tab,
        DocumentsTab.MAILINGS: DocumentsPage(context).open_mailings_tab,
        DocumentsTab.TAXES: DocumentsPage(context).open_taxes_tab,
    }
    if tab in tab_mapping:
        tab_mapping[tab]()
    else:
        raise AutomationException(f"There is no such tab as {tab}.")
    log.info(f"{tab} is opened.")


@when('I filter "{tab}" by date using "{value}" on the Documents page')
def filter_table_date(context, tab, value):
    tab = tab.lower()
    year = value if re.match(r"\b\d{4}\b", value) else "Null"
    filter_value_mapping = {
        "all": "All",
        "last 30 days": "Last_30_Days",
        "last 90 days": "Last_90_Days",
        "current year": "Current_Year",
        "last year": "Last_Year",
        year: value,
    }
    if value.lower() in filter_value_mapping:
        filter_value = filter_value_mapping[value.lower()]
        DocumentsStepHelper().get_documents_tab(context, tab).get_date_filter().select(value=filter_value)
    else:
        raise AutomationException(f"There is no such option as {value}")


@when('I filter "{tab}" by "{filter_name}" "{value}" on the Documents page')
def filter_document_table(context, tab, filter_name, value):
    value = BehaveHelper().format_context(context, value)
    tab = tab.lower()
    document_tab = DocumentsStepHelper().get_documents_tab(context, tab)
    documents_filter = DocumentsStepHelper().get_document_filter(document_tab, filter_name)
    documents_filter.select(value=value)


@when('I click on the "{index}" document with "{account_number}" account number on the "{page}" Page')
def open_document_by_account_number_and_index(context, index, account_number, page):
    account_number = BehaveHelper.format_context(context, account_number)
    index = StringHelper().word_to_number(index)
    match page.lower():
        case "dashboard":
            rows = DashboardPage(context).get_documents_table().get_rows()
        case "documents":
            rows = DocumentsPage(context).get_statements_tab().get_table().get_rows()
        case _:
            raise AutomationException(f"The are no such options as {page}.")
    matching_rows = [row for row in rows if account_number in row.text]
    matching_rows[int(index) - 1].click()


@then("The document PDF preview is opened")
def verify_pdf_is_opened(context):
    context.browser.switch_to_tab(DocumentsPreviewPage(context).endpoint)
    pdf_element = DocumentsPreviewPage(context).get_pdf_element()
    document_type = pdf_element.get_attribute("type")
    Assert.contains("pdf", document_type, "PDF preview is not opened.")
    log.info("PDF preview is opened.")


@then('The Documents "{filter_name}" filter on "{tab}" contains unique names from table')
def verify_unique_names_in_documents_filter(context, filter_name, tab):
    documents_tab = DocumentsStepHelper().get_documents_tab(context, tab)
    rows = documents_tab.get_table().extract_cells_data(0)
    row_data = DocumentsStepHelper().convert_row_object(rows, tab)
    filter_item = FilterType(filter_name.lower())
    if filter_item == FilterType.ACCOUNTS:
        unique_values = list(set([row.get_account_filter_format() for row in row_data]))
    elif filter_item == FilterType.TAX_YEAR:
        if DocumentsTab(tab.lower()) != DocumentsTab.TAXES:
            raise AutomationException(f"There is no tax year filter for {tab}")
        unique_values = list(set([year_row[0] for year_row in rows.items()]))
    else:
        unique_values = list(set([row.name for row in row_data]))
    filter_values = DocumentsStepHelper().get_document_filter(documents_tab, filter_name).get_option_texts()
    Assert.is_equal(sorted(filter_values[1:]), sorted(unique_values))


@when('I filter documents "{documents}" from API response by "{criteria}" "{value}" and save it as "{new_variable}"')
def filter_documents_by_criteria(context, documents, criteria, value, new_variable):
    value = BehaveHelper().format_context(context, value)
    filtered_documents = DocumentsStepHelper().filter_api_documents(context, criteria, value, documents)
    setattr(context, new_variable, filtered_documents)


@then('The documents "{tab}" table contains "{documents}" items')
def verify_documents_table_contains(context, tab, documents):
    document_list = documents if isinstance(documents, list) else getattr(context, documents)
    doc_object = DocumentsStepHelper().convert_to_documents_object(document_list)
    expected_doc = DocumentsStepHelper().filter_documents(doc_object, tab)
    actual_rows = DocumentsStepHelper().get_documents_tab(context, tab).get_table().extract_cells_data()
    actual_rows_object = DocumentsStepHelper().convert_row_object(actual_rows, tab)
    Assert.is_equal(
        len(expected_doc),
        len(actual_rows_object),
        f"Count of items on UI is different from API. Expected - {len(expected_doc)}, "
        f"but actual - {len(actual_rows_object)}",
    )

    match DocumentsTab(tab.lower()):
        case DocumentsTab.STATEMENTS:
            expected_doc_formatted = [doc.get_statements_format() for doc in expected_doc]
        case DocumentsTab.TAXES:
            expected_doc_formatted = [doc.get_tax_format() for doc in expected_doc]
        case DocumentsTab.MAILINGS:
            expected_doc_formatted = [doc.get_mailing_format() for doc in expected_doc]
        case DocumentsTab.REPORTS:
            expected_doc_formatted = [doc.get_report_format() for doc in expected_doc]
        case _:
            raise AutomationException(f"The are no such tab as {tab}.")

    Assert.is_equal(actual_rows_object, expected_doc_formatted)


@then('The Documents "{filter_name}" filter options on "{tab}" can filter "{documents}" correctly')
def verify_documents_filtering(context, filter_name, tab, documents):
    document_tab = DocumentsStepHelper().get_documents_tab(context, tab)
    documents_filter = DocumentsStepHelper().get_document_filter(document_tab, filter_name)
    filter_values = documents_filter.get_option_values()
    for value in filter_values[1:]:
        documents_filter.select(value=value)
        expected_filtered_docs = DocumentsStepHelper().filter_api_documents(context, filter_name, value, documents)
        verify_documents_table_contains(context, tab, expected_filtered_docs)


@then('The are no "{documents}" Documents on "{tab}" tab')
def verify_no_documents(context, documents, tab):
    document_list = documents if isinstance(documents, list) else getattr(context, documents)
    doc_object = DocumentsStepHelper().convert_to_documents_object(document_list)
    expected_doc = DocumentsStepHelper().filter_documents(doc_object, tab)
    try:
        Assert.is_equal(expected_doc, [])
    except AssertionError:
        raise AutomationException(f"There are some documents on {tab} tab. Please verify test data")
    document_tab = DocumentsStepHelper().get_documents_tab(context, tab)
    is_no_documents_present = document_tab.is_no_documents_present()
    Assert.is_true(is_no_documents_present)


class DocumentsStepHelper:
    @staticmethod
    def filter_documents(documents_object, tab):
        doc_type_mapping = {
            DocumentsTab.STATEMENTS: "STATEMENT",
            DocumentsTab.TAXES: "TAX DOCUMENT",
            DocumentsTab.MAILINGS: "GENERAL CORRESPONDENCE",
            DocumentsTab.REPORTS: "Performance Report",
        }
        tab_name = DocumentsTab(tab.lower())
        doc_type = doc_type_mapping.get(tab_name)
        if doc_type is None:
            raise AutomationException(f"There are no such tab as {tab}.")
        return [document for document in documents_object if document.type == doc_type]

    @staticmethod
    def filter_api_documents(context, criteria, value, documents):
        document_list = documents if isinstance(documents, list) else getattr(context, documents)
        doc_object = DocumentsStepHelper().convert_to_documents_object(document_list)
        if criteria.lower() == FilterType.DATE.value:
            match value.lower():
                case "all":
                    filter_value = None
                case "last 30 days":
                    filter_value = DateHelper.get_last_days(30, "%b %d, %Y")
                case "last 90 days":
                    filter_value = DateHelper.get_last_days(90, "%b %d, %Y")
                case "current year":
                    filter_value = DateHelper.get_year_dates(DateHelper.get_year())
                case "last year":
                    filter_value = DateHelper.get_year_dates(DateHelper.get_year(1))
                case _ if re.match(r"\b\d{4}\b", value):
                    filter_value = DateHelper.get_year_dates(int(value))
                case _:
                    raise AutomationException(f"There is no such option as {value}")
            if filter_value is None:
                filtered_documents = doc_object  # No need to filter
            else:
                filtered_documents = [doc for doc in doc_object if doc.date in filter_value]
        elif criteria.lower() == FilterType.ACCOUNTS.value:
            filtered_documents = [doc for doc in doc_object if doc.account_number == value]
        elif criteria.lower() == FilterType.TYPE.value:
            filtered_documents = [doc for doc in doc_object if doc.name == value]
        else:
            raise AutomationException(f"There is no such filter criteria as {criteria}")
        return filtered_documents

    @staticmethod
    def convert_to_documents_object(document_list):
        documents_object = (
            document_list
            if isinstance(next((document for document in document_list), None), DocumentsApiModel)
            else [DocumentsApiModel(**item) for item in document_list]
        )
        log.info("The document list is saved as an object.")
        return documents_object

    @staticmethod
    def convert_row_object(rows, tab_name):
        data = []
        for year_row in rows.items():
            match DocumentsTab(tab_name.lower()):
                case DocumentsTab.STATEMENTS:
                    data.extend(
                        [
                            StatementsRowModel(date, year_row[0], account, name)
                            for date, account, name in rows[year_row[0]]
                        ]
                    )
                case DocumentsTab.REPORTS:
                    data.extend(
                        [
                            ReportsRowModel(quarter, year_row[0], account, name)
                            for quarter, account, name in rows[year_row[0]]
                        ]
                    )
                case DocumentsTab.MAILINGS:
                    data.extend(
                        [MailingsRowModel(date, year_row[0], account, name) for date, account, name in rows[year_row[0]]]
                    )
                case DocumentsTab.TAXES:
                    data.extend([TaxesRowModel(name, year_row[0], account) for name, account in rows[year_row[0]]])
                case _:
                    raise AutomationException(f"The are no such tab as {tab_name}.")
        return data

    @staticmethod
    def get_documents_tab(context, tab_name):  # noqa: CFQ004
        match (DocumentsTab(tab_name.lower())):
            case DocumentsTab.STATEMENTS:
                return DocumentsPage(context).get_statements_tab()
            case DocumentsTab.REPORTS:
                return DocumentsPage(context).get_reports_tab()
            case DocumentsTab.MAILINGS:
                return DocumentsPage(context).get_mailings_tab()
            case DocumentsTab.TAXES:
                return DocumentsPage(context).get_taxes_tab()
            case _:
                raise AutomationException(f"There are no such tab as {tab_name}.")

    @staticmethod
    def get_document_filter(tab, filter_name):  # noqa: CFQ004
        filter_type = FilterType(filter_name.lower())
        if isinstance(tab, ReportsTab) and filter_type != FilterType.DATE:
            raise AutomationException("Report Tab has date filter only")
        if filter_type in {FilterType.DATE, FilterType.TAX_YEAR}:
            return tab.get_date_filter()
        elif filter_type == FilterType.ACCOUNTS:
            return tab.get_account_filter()
        elif filter_type == FilterType.TYPE:
            return tab.get_type_filter()
        else:
            raise AutomationException(f"There are no such filter as {filter_name}.")
