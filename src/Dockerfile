FROM python:3-alpine

COPY . .

ENV FLASK_APP=lazyAPI
ENV FLASK_ENV=development
RUN pip3 install -e .

CMD flask run --host=0.0.0.0