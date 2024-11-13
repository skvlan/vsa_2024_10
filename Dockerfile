FROM python:3.11-rc-slim

RUN apt update
RUN mkdir /carmarket

WORKDIR /carmarket

COPY ./src ./src
COPY ./requirements.txt ./requirements.txt
COPY ./commands ./commands

RUN python -m pip install --upgrade pip && pip install -r ./requirements.txt

# CMD ["python", "src/manage.py", "runserver", "0:8008"]
CMD ["bin/bash"]