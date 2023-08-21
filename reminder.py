from slack_bolt.adapter.socket_mode import SocketModeHandler
import schedule
import time
import json
from slack_bolt import App
import os
from datetime import datetime as dt

app = App(token=os.environ.get('SLACK_TOKEN'))
appointment = {
    "date": dt.today().date().strftime("%d/%m/%Y"),
    "number": 1,
}

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


def morning_reminder():
    appointment = update_today_appointment()
    response_text = "Hi have a greate day, Today is {}, today is the {} and {} turns to make tea".format(
        appointment['date'],
        persons[str(appointment['number'])][0], persons[str(appointment['number'])][1])
    print('running')
    app.client.chat_postMessage(channel='#tea_time_notif', text=response_text)


def tommorow_reminder():
    appointment = update_today_appointment()
    response_text = "Hi have a greate day, Today is {}, tommorow is the {} and {} turns to make tea".format(
        appointment['date'],
        persons[str(appointment['number'] + 1)][0], persons[str(appointment['number'] + 1)][1])


schedule.every().day.at("08:00").do(morning_reminder, 'Asia/Tehran')
schedule.every().day.at("17:00").do(tommorow_reminder, 'Asia/Tehran')

while True:
    schedule.run_pending()
    time.sleep(1)
