FROM python:3

RUN pip install requests
RUN pip install lxml

ADD *.py /
ADD payloads.xss /

ENTRYPOINT ["python", "./xss-detector.py"]

