# text_toolkit\cleaner.py
import re
from bs4 import  BeautifulSoup
from .logger import logger  # 导入logger

def clean_text(text):
    try:
        # 使用BeautifulSoup去掉HTML标签
        soup = BeautifulSoup(text, "html.parser")
        cleaned_text = soup.get_text()
        cleaned_text = cleaned_text.replace('\xa0', ' ')  # 替换非断空格字符

        # 使用正则表达式去掉中文字符之间的所有空白字符（不包括换行），但保留英文字符之间的空格
        cleaned_text = re.sub(
            r"(?<=[\u4e00-\u9fff]) +(?=[\u4e00-\u9fff])", "", cleaned_text)

        # 去除换行符周围的空格
        cleaned_text = re.sub(r" *\n *", "\n", cleaned_text)

        # 去除首尾空白字符
        cleaned_text = cleaned_text.strip()
        cleaned_text = re.sub(r"\n+", "\n", cleaned_text)

        return cleaned_text
    except Exception as e:
            logger.error(f"An error occurred while cleaning text: {e}")
            raise