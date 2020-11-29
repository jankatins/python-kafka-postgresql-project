FROM python:3.8-slim-buster

RUN ["mkdir", "-p", "/checkweb"]
WORKDIR /src

RUN groupadd -r checkweb && useradd --no-log-init -r -g checkweb checkweb

COPY ./src/ /src/
COPY requirements.txt.freeze /src/

RUN true \
    && pip install --upgrade pip \
    && pip install --no-cache-dir  -r requirements.txt.freeze

USER checkweb

# start by default as producer
ENTRYPOINT ["python3", "-m", "checkweb"]
CMD ["producer"]
