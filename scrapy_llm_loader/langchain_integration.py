from scrapy.statscollectors import StatsCollector
import json

from .langchain_api import create_langchain_model, invoke_langchain_api
from .prompt import create_prompt
from .output_parser import create_item_parser
from .utils import CleaningMode

total_tokens = 0


def extract_from_html(
    html_content: str,
    item_class,
    openai_api_key: str,
    stats_collector: StatsCollector,
    cleaning_mode: CleaningMode,
):
    global total_tokens

    model = create_langchain_model(openai_api_key)
    item_parser = create_item_parser(item_class)
    prompt = create_prompt(item_parser, html_content, cleaning_mode)

    output, tokens = invoke_langchain_api(model, prompt)
    total_tokens += tokens

    update_scrapy_stats(stats_collector, total_tokens)

    return json.loads(output.content)


def update_scrapy_stats(stats_collector: StatsCollector, token_count: int):
    stats_collector.set_value("total_tokens", token_count)
