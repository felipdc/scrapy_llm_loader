from langchain.output_parsers import PydanticOutputParser


def create_item_parser(item_class):
    return PydanticOutputParser(pydantic_object=item_class)
