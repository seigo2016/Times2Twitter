FROM python:3.7
RUN mkdir src
COPY src src/
WORKDIR ./src/
RUN python -m pip install slackclient slackeventsapi
CMD [ "python", "Start.py" ]
