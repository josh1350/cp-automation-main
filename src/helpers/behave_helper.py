import re

from src.helpers.string_helper import StringHelper


class BehaveHelper:
    @staticmethod
    def format_context(context, string):  # noqa: FNE008
        pattern = r"(\{\$.*?\})"
        variable_names = re.findall(pattern, string)
        for variable in variable_names:  # noqa: VNE002
            variable_name = variable.strip("{$}")
            value = getattr(context, variable_name)
            string = string.replace(variable, value)
        return StringHelper().normalize(string)

    @staticmethod
    def get_tc_id(tags):
        tc_id = None
        for tag in tags:
            match = re.search(r"link.*:(\w+-\w+)", tag)
            if match:
                tc_id = match.group(1)
        return tc_id
