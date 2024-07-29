import re

from html.parser import HTMLParser as _html_parser
from io import StringIO as _string_io


class StripHTML(_html_parser):
    def __init__(self) -> None:
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = _string_io()

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()

    def strip(self, html: str | int | list) -> str:
        self.feed(str(html))

        stripped = self.get_data()
        return stripped

    def abbreviate(self, text: str, max_len: int | None = 100) -> str:
        # replace line breaks and tabs with spaces
        text = text.replace("\r", " ")
        text = text.replace("\n", " ")
        text = text.replace("\t", " ")

        # remove repetitive spaces
        text = re.sub(r" +", " ", text)
        if max_len:
            text = text[:max_len]
        return text

    def __call__(self, html: str | int | list, max_len: int = 100) -> str:
        result = self.strip(html)
        result = self.abbreviate(result, max_len)
        return result
