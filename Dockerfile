FROM python:3.11.4

RUN pip install requests

CMD cd /web-scrapper && python main.py