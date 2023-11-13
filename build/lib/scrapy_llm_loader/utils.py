from bs4 import BeautifulSoup, Comment
import re

def clean_html(html_content: str):
    soup = BeautifulSoup(html_content, 'html.parser')

    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()
        
    for script_or_style in soup(['script', 'style']):
        script_or_style.extract()

    for tag in soup(True):
        unwanted_attributes = ['style', 'onclick', 'onmouseover', 'onmouseout', 'onkeydown', 'onkeyup']
        for attribute in unwanted_attributes:
            del tag[attribute]

    cleaned_html = str(soup)

    cleaned_html = re.sub(r'\n\s*\n', '\n', cleaned_html)

    return cleaned_html
  