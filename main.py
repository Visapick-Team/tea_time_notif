import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import json
from datetime import datetime as dt

appointment = {
    "date": dt.today().date().strftime("%d/%m/%Y"),
    "number": 1,
}

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
# app.client.chat_scheduleMessage()
with open('persons.json') as f:
    persons = json.load(f)
    len_persons = len(persons)
    print(len_persons)


def update_today_appointment():
    today_dt = dt.today().date()
    today = today_dt.strftime("%d/%m/%Y")
    if not os.path.exists('appointments.json'):
        with open('appointments.json', 'w') as f:
            json.dump([appointment], f)
    else:
        with open('appointments.json') as f:
            appointments = json.load(f)
            today_str = dt.today().date().strftime("%d/%m/%Y")
        if appointments['date'] != today_str:
            appointments['date'] = today_str
            appointments['number'] = appointments['number'] + 1
            if appointments['number'] > len_persons:
                appointments['number'] = 1
            with open('appointments.json', 'w') as f:
                json.dump(appointments, f)
            return appointments
        return appointments


@app.command("/today")
def tea_today(ack, respond, command):
    # Acknowledge command request
    ack()
    appointment = update_today_appointment()

    # get today appointment
    response_text = "Hi have a greate day, Today is {}, today is the {} and {} turns to make tea".format(
        appointment['date'],
        persons[str(appointment['number'])][0], persons[str(appointment['number'])][1])
    respond(response_text)


@app.command('/tomorrow')
def tea_tomorrow(ack, respond, command):
    # Acknowledge command request
    ack()
    respond("Hi")
    # update today appointment
    appointment = update_today_appointment()

    respond(
        f"Hi have a greate day, Today is {appointment['date']}, tomorrow is the {persons[str(appointment['number'] + 1)]} turn to make tea")


if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
