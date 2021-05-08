# This Dockerfile is meant to be used for production only!

FROM python:latest
RUN mkdir code
RUN mkdir uploads
RUN mkdir requirements
RUN mkdir scripts
COPY requirements.txt /
COPY src /code
COPY scripts /scripts
RUN chmod +x /scripts/runserver.sh
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip3 install opencv-python
RUN pip3 install profanity-filter
RUN pip3 install -r requirements.txt
RUN python3 -m spacy download en
WORKDIR /code
CMD ["/scripts/runserver.sh"]