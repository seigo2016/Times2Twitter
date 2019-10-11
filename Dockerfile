FROM python:3
RUN mkdir src
ARG btoken
ARG utoken
ENV SlackBtoken=$btoken
ENV SlackUtoken=$utoken
COPY src src/
WORKDIR ./src/
RUN python -m pip install   slackclient
CMD [ "python", "Start.py" ]
