from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.callbacks import get_openai_callback
from langchain.pydantic_v1 import BaseModel
from scrapy.statscollectors import StatsCollector

from .utils import clean_html
import json


total_tokens = 0
num_items = 0


def extract_from_html(html_content: str, item: BaseModel, openai_api_key: str, stats_collector: StatsCollector):
  global total_tokens, num_items

  model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=openai_api_key)
  parser = PydanticOutputParser(pydantic_object=item)
  
  template = "You generate the output based on the HTML provided.\n{format_instructions}\n"
  system_message_prompt = SystemMessagePromptTemplate.from_template(template)
  
  human_template="{query}"
  human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

  prompt = ChatPromptTemplate(
      input_variables=["query"],
      messages=[
        system_message_prompt,
        human_message_prompt,
      ],
      partial_variables={"format_instructions": parser.get_format_instructions()},
  )

  _input = prompt.format_prompt(query=clean_html(html_content))

  with get_openai_callback() as cb:
    output = (model.invoke(_input.to_string()))
    total_tokens += cb.total_tokens

  update_scrapy_stats(stats_collector, total_tokens)

  return json.loads(output.content)

def get_total_tokens():
    return total_tokens

def update_scrapy_stats(stats_collector: StatsCollector, token_count: int):
    current_count = stats_collector.get_value('total_tokens', 0)
    stats_collector.set_value('total_tokens', current_count + token_count)
