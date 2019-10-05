FROM python:3
ENV SlackUtoken xoxp-765247246691-776724231301-770988621345-c2dc7dba1595ea9ca1b10ae85b15a136
ENV SlackBtoken  xoxb-17948093585-783625396624-RFoYj0Qk4MnXw3O4kxBkfSVE
RUN mkdir src
COPY src src/
WORKDIR ./src/
RUN python -m pip install   slackclient
CMD [ "python", "Start.py" ]
