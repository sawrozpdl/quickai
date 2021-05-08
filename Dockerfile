# This Dockerfile is meant to be used for production only!

FROM python:latest
RUN mkdir code
RUN mkdir requirements
RUN mkdir scripts
COPY requirements.txt /
COPY src /code
COPY script /scripts
RUN chmod +x /scripts/runserver.sh
RUN pip install -r requirements.txt
RUN python -m spacy download en
WORKDIR /code
CMD ["/scripts/runserver.sh"]