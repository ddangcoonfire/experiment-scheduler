FROM python:3.9

RUN pip install update
COPY . .

RUN pip install -r requirement.txt

RUN pip install -e .

ENTRYPOINT ["exs", "init_master"]
