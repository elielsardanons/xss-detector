FROM python:3

RUN pip install requests

ADD *.py /
ADD payloads.xss /

ENTRYPOINT ["python", "./xss-detector.py"]

