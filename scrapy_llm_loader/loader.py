import os
from scrapy.utils.project import get_project_settings

from .langchain_integration import extract_from_html
from .utils import CleaningMode


class LangChainLoader:
    def __init__(self, item_class, response, crawler, openai_api_key=None):
        self.item_class = item_class
        self.response = response
        self.crawler = crawler
        settings = get_project_settings()
        self.openai_api_key = (
            openai_api_key
            or os.getenv("OPENAI_API_KEY")
            or settings.get("OPENAI_API_KEY")
        )

        if not self.openai_api_key:
            raise ValueError("OpenAI API key not provided or found in settings.")

    def load_item(self, cleaning_mode=CleaningMode.DEFAULT):
        extracted_data = extract_from_html(
            self.response.text,
            self.item_class,
            self.openai_api_key,
            self.crawler.stats,
            cleaning_mode,
        )
        return self.item_class(**extracted_data)
