FROM python:3.7.4-slim-buster

RUN pip install slack_bolt
RUN pip install schedule
RUN pip install pytz
WORKDIR /app
COPY reminder.py /app
COPY persons.json /app
COPY appointments.json /app
CMD ["python", "reminder.py"]