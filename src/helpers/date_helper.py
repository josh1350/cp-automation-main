import datetime


class DateHelper:
    @staticmethod
    def get_year(year_offset=0):
        current_year = datetime.datetime.now().year
        target_year = current_year - year_offset
        return target_year

    @staticmethod
    def get_quarter(date):
        date_object = datetime.datetime.strptime(date, "%b %d")
        quarter = (date_object.month - 1) // 3 + 1
        return f"Q{quarter}"

    @staticmethod
    def get_last_days(days_count, format_pattern="%b %d"):
        current_date = datetime.datetime.now()
        formatted_dates = []
        for day_offset in range(days_count, 0, -1):
            delta = datetime.timedelta(days=day_offset)
            target_date = current_date - delta
            formatted_date = target_date.strftime(format_pattern)
            formatted_dates.append(formatted_date)
        return formatted_dates

    @staticmethod
    def get_year_dates(year):
        start_date = datetime.datetime(year, 1, 1)
        end_date = datetime.datetime(year, 12, 31)
        dates = []

        while start_date <= end_date:
            formatted_date = start_date.strftime("%b %d, %Y")
            dates.append(formatted_date)
            start_date += datetime.timedelta(days=1)

        return dates

    @staticmethod
    def convert_date(date, date_format="%b %d, %Y"):  # noqa: FNE008
        parsed_date = datetime.datetime.fromisoformat(date)
        formatted_date = parsed_date.strftime(date_format)
        return formatted_date
