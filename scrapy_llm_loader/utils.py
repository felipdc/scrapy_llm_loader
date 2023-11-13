from bs4 import BeautifulSoup, Comment
import re
from enum import Enum


class CleaningMode(Enum):
    DEFAULT = 1
    TEXT_ONLY = 2


def clean_html(html_content: str, mode: CleaningMode = CleaningMode.DEFAULT):
    soup = BeautifulSoup(html_content, "html.parser")

    if mode == CleaningMode.DEFAULT:
        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()

        for script_or_style in soup(["script", "style"]):
            script_or_style.extract()

        for tag in soup(True):
            unwanted_attributes = [
                "style",
                "onclick",
                "onmouseover",
                "onmouseout",
                "onkeydown",
                "onkeyup",
            ]
            for attribute in unwanted_attributes:
                del tag[attribute]

        cleaned_html = str(soup)

        cleaned_html = re.sub(r"\n\s*\n", "\n", cleaned_html)

        return cleaned_html

    if mode == CleaningMode.TEXT_ONLY:
        return soup.get_text()
