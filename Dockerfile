FROM python:3.8-slim

RUN pip install pipenv

COPY Pipfile /
COPY Pipfile.lock /

RUN pipenv install --system --deploy --ignore-pipfile

COPY . /

WORKDIR /data
CMD /app.py