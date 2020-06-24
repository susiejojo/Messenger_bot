from .fb_requests import *
from .quick_replies import generate_dates, generate_slots, generate_reminder_slots
import datetime

def book_appointment(value, recipient_id, db):
    if value == "":
        dates = db.appointment.distinct("date",{"appointment_status" : "0"})
        dates_remove = []
        delta = datetime.timedelta(days=1)
        for i in dates:
            temp_date = datetime.datetime.strptime(i,"%d.%m.%Y")
            if (temp_date < (datetime.datetime.now()-delta)):
                dates_remove.append(i)
        for i in dates_remove:
            dates.remove(i)
        if (len(dates)>7):
            dates=dates[:7]
        if (len(dates)==0):
            payload = {
                "message": {
                    "text": "I'm really sorry, I can't find any available slot!"
                },
                "recipient": {"id": recipient_id},
                "messaging_type": "RESPONSE",
                "notification_type": "regular",
            }
        else:
            payload = {
                "message": {
                    "text": "Pick a date when you'll be available:",
                    "quick_replies": generate_dates(dates),
                },
                "recipient": {"id": recipient_id},
                "messaging_type": "RESPONSE",
                "notification_type": "regular",
        }
        return payload
    elif value.startswith("date"):
        selected_date = value.split(" ")[-1]
        print(selected_date)
        slots = db.appointment.distinct("time", {"date" : selected_date})
        print(slots)
        payload = {
            "message": {
                "text": "Pick a time slot when you'll be available:",
                "quick_replies": generate_slots(slots,selected_date),
            },
            "recipient": {"id": recipient_id},
            "messaging_type": "RESPONSE",
            "notification_type": "regular",
        }
        print(payload)
        return payload
    elif value.startswith("time"):
        selected_date = value.split(" ")[1]
        selected_time = value.split(" ")[2]
        print(selected_date,selected_time)
        db.appointment.update_one({"date": selected_date, "time": selected_time}, {"$set": {"appointed_id": recipient_id, "appointment_status" : "1"}})
        app_time = datetime.datetime.strptime(
                selected_time, "%H:%M"
            )
        payload = {
            "recipient": {"id": recipient_id},
            "messaging_type": "RESPONSE",
            "message": {
                "text": "Pick a reminder time:",
                "quick_replies": generate_reminder_slots(app_time, selected_date),
            },
        }
        print(payload)
        return payload
    elif value.startswith("reminder"):
        print(value)
        payload = {
                "recipient": {"id": recipient_id},
                "message": {
                    "attachment": {
                        "type": "template",
                        "payload": {
                            "template_type": "one_time_notif_req",
                            "title": 'Select "notify me" to confirm the reminder?',
                            "payload": value,
                        },
                    }
                },
            }
        print(payload)
        return payload