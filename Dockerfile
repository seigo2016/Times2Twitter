FROM python:3
ENV SlackUtoken $SlackUtoken
ENV SlackBtoken $SlackBtoken
RUN mkdir src
COPY src src/
WORKDIR ./src/
RUN python -m pip install   slackclient
CMD [ "python", "Start.py" ]
