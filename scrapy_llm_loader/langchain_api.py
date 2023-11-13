from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback


def invoke_langchain_api(model, input_string):
    with get_openai_callback() as cb:
        output = model.invoke(input_string)
        total_tokens = cb.total_tokens
    return output, total_tokens


def create_langchain_model(openai_api_key: str):
    return ChatOpenAI(
        model_name="gpt-3.5-turbo", temperature=0, openai_api_key=openai_api_key
    )
