from setuptools import setup, find_packages # pip install setuptools
from io import open


def read(filename):
   """Прочитаем наш README.md для того, чтобы установить большое описание."""
   with open(filename, "r", encoding="utf-8") as file:
      return file.read()


setup(name="TUOP",
   version="0.0.6", # Версия твоего проекта. ВАЖНО: менять при каждом релизе
   description="for ege",
   long_description=read("README.md"), # Здесь можно прописать README файл с длинным описанием
   long_description_content_type="text/markdown", # Тип контента, в нашем случае text/markdown
   author="UshliyOrk",
   author_email="pavel.pilgun.accounts@yandex.ru",
   url="https://github.com/Fsoky/Upload-library-to-PyPI", # Страница проекта
   keywords="api some_keyword tools", # Ключевые слова для упрощеннего поиска пакета на PyPi
   packages=find_packages() # Ищем пакеты, или можно передать название списком: ["package_name"]
)