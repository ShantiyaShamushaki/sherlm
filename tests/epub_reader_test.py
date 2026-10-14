import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import re


def extract_epub_text(path):
    book = epub.read_epub(path)
    chapters = []
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        soup = BeautifulSoup(item.get_content(), 'html.parser')
        # حذف تگ‌های اضافی
        for tag in soup(['script', 'style']):
            tag.decompose()
        text = soup.get_text(separator='\n')
        # نرمال‌سازی
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = text.strip()
        if text:
            chapters.append(text)
    return '\n\n'.join(chapters)

text = extract_epub_text('data/hafez.epub')
with open('hafez_test.txt', 'w', encoding='utf-8') as f:
    f.write(text)