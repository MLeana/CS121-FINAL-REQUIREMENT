import json
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

from telegram import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import (
    Updater,
    Filters,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
)

load_dotenv()

main_keyboard = [
    ["➕ Add Reminder", "➖ Delete History"],
    ["📃 All Reminders", "🌐 Change UTC"],
    ["💰 Donate"],
]

REMINDER_TITLE, REMINDER_DATE, REMINDER_TIME, REMINDER_INFO = range(4)
DELETE_REMINDER_INDEX = range(1)
ADD_UTC = range(1)

def is_new_user(user, username, first_name, last_name):
    user = str(user)
    with open("data.json", "r+") as file:
        content = json.load(file)
        if user not in content["users"]:
            content["users"][user] = {
                "username": username,
                "first name": first_name,
                "last name": last_name,
                "utc": "",
                "reminders": [],
            }
            file.seek(0)
            json.dump(content, file)
            file.truncate()

            return True
        else:
            return False


def json_add_utc(user, utc):
    user = str(user)
    with open("data.json", "r+") as file:
        content = json.load(file)
        content["users"][user]["utc"] = utc
        file.seek(0)
        json.dump(content, file)
        file.truncate()

def json_get_utc(user):
    user = str(user)
    with open("data.json", "r") as file:
        content = json.load(file)
        return content["users"][user]["utc"]


def json_get_info(user):
    user = str(user)
    with open("data.json", "r") as file:
        content = json.load(file)
        return content["users"][user]["reminders"][0]


def json_add_reminder(user):
    user = str(user)
    with open("data.json", "r+") as file:
        content = json.load(file)
        content["users"][user]["reminders"].insert(
            0, {"title": "", "date": "", "time": "", "info": ""}
        )
        file.seek(0)
        json.dump(content, file)
        file.truncate()


def json_add_reminder_info(user, key, value):
    user = str(user)
    key = str(key)
    with open("data.json", "r+") as file:
        content = json.load(file)
        content["users"][user]["reminders"][0][key] = value
        file.seek(0)
        json.dump(content, file)
        file.truncate()


def json_cancel_add_reminder_process(user):
    user = str(user)
    with open("data.json", "r+") as file:
        content = json.load(file)
        del content["users"][user]["reminders"][0]
        file.seek(0)
        json.dump(content, file)
        file.truncate()


def json_delete_reminder(user, index):
    user = str(user)
    index = index - 1

    with open("data.json", "r+") as file:
        content = json.load(file)

        del content["users"][user]["reminders"][index]
        file.seek(0)
        json.dump(content, file)
        file.truncate()


def json_get_reminders_list(user):
    user = str(user)
    with open("data.json", "r+") as file:
        content = json.load(file)
        content = content["users"][user]["reminders"]

        if len(content) == 0:
            message = "📪 You have no reminders!"
            return message

        else:
            message = ""
            for i in range(len(content)):
                title = content[i]["title"]
                date = content[i]["date"]
                time = content[i]["time"]
                info = content[i]["info"]

                message += f"""
*Reminder {i+1}*
------------------
_Title_ : {title}
_Date_ : {date}
_Time_ : {time}
_Info_ : {info}
"""
            return message

        
