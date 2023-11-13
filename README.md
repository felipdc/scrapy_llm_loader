# scrapy_llm_loader

`scrapy_llm_loader` is a Scrapy extension that enables data extraction using LangChain, a technology that leverages large language models (LLMs) like OpenAI's GPT models.

## Features

- **Integration with LangChain**: Utilizes LangChain to process HTML content and extract structured data.
- **OpenAI GPT Model Support**: Compatible with OpenAI's GPT models, providing high-quality content extraction.
- **Scrapy Compatibility**: Seamlessly integrates with existing Scrapy projects, enhancing them with advanced LLM capabilities.

## Installation

`scrapy_llm_loader` can be easily installed using `pip`. Just run the following command:

```bash
pip install scrapy_llm_loader
```


## Note
Before using `scrapy_llm_loader`, ensure that the `OPENAI_API_KEY` is set in your project's `settings.py` or passed explicitly as an argument with `openai_api_key` during the loader's initialization.

## Usage
To use `scrapy_llm_loader` in your Scrapy project:
1. Import `LangChainLoader` from `scrapy_llm_loader.loader`.
2. Define your item model using Pydantic.
3. Create an instance of `LangChainLoader` in your spider and use it to load items.

Example:

```python
from scrapy_llm_loader.loader import LangChainLoader
from pydantic import BaseModel, Field

class MyItem(BaseModel):
    name: str = Field(description="name of the product")
    price: str = Field(description="price of the product")
    # Describe other fields here
    pass

class MySpider(scrapy.Spider):
    # Your spider definition
    def parse(self, response):
        loader = LangChainLoader(item_class=MyItem, response=response, crawler=self.crawler)
        item = loader.load_item()
        yield item.dict()
```



