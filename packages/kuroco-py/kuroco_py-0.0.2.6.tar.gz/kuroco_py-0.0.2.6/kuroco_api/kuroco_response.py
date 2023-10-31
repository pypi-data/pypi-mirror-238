from pandas import DataFrame

from .CONFIG import COLUMN_NAME_FOR_TOPICS_ID

DEFAULT_DATA_KEYWORD = "list"

class KurocoResponse:
    _status: int
    _data: DataFrame

    _errors: list = []
    _messages: list = []
    _debug_output: str = ""
    _page_info: dict = {}

    def __init__(self, status: int, values: dict):
        self.status = status
        self.errors = values.pop("errors", None)
        self.messages = values.pop("messages", None)
        self.debug_output = values.pop("debug_output", None)
        self.page_info = values.pop("page_info", None)
        self.data = values[DEFAULT_DATA_KEYWORD]

    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, value: int):
        assert isinstance(value, int), "Status must be an integer"
        self._status = value

    @property
    def errors(self):
        return self._errors
    
    @errors.setter
    def errors(self, value: list):
        if value is not None:
            assert isinstance(value, list), "Errors must be a list"
            self._errors = value

    @property
    def messages(self):
        return self._messages
    
    @messages.setter
    def messages(self, value: list):
        if value is not None:
            assert isinstance(value, list), "Messages must be a list"
            self._messages = value

    @property
    def debug_output(self):
        return self._debug_output
    
    @debug_output.setter
    def debug_output(self, value: str):
        if value is not None:
            assert isinstance(value, str), "Debug output must be a string"
            self._debug_output = value

    @property
    def page_info(self):
        return self._page_info
    
    @page_info.setter
    def page_info(self, value: dict):
        if value is not None:
            assert isinstance(value, dict), "Page info must be a dict"
            self._page_info = value

    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, value: list):
        assert isinstance(value, list), "Data must be a list"
        self._data = DataFrame(value).set_index(COLUMN_NAME_FOR_TOPICS_ID)
    