from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from .utils import clean_html


def create_prompt(item_parser, html_content, cleaning_mode):
    template = (
        "You generate the output based on the HTML provided.\n{format_instructions}\n"
    )
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)

    human_template = "{query}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    prompt = ChatPromptTemplate(
        input_variables=["query"],
        messages=[
            system_message_prompt,
            human_message_prompt,
        ],
        partial_variables={
            "format_instructions": item_parser.get_format_instructions()
        },
    )

    _input = prompt.format_prompt(query=clean_html(html_content, cleaning_mode))
    return _input.to_string()
