FROM python:3

RUN pip install requests

ADD *.py /

ENTRYPOINT ["python", "./xss-detector.py"]

