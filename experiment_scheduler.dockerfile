FROM python:3.9

RUN pip install update
ADD requirement.txt requirement.txt
RUN pip install -r requirement.txt

COPY . .
RUN pip install -e .
