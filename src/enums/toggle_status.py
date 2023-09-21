from enum import Enum


class ToggleStatus(Enum):
    HIDDEN = "visibility_off"
    SHOWN = "visibility"

    @classmethod
    def from_string(cls, status_str):
        if status_str.lower() == "show":
            return cls.SHOWN
        elif status_str.lower() == "hide":
            return cls.HIDDEN
        else:
            raise ValueError("Invalid status string")
