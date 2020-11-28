import json
import time
import os

import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from dotenv import load_dotenv
load_dotenv()

POST_ID = os.getenv('POST_ID')
TOKEN = os.getenv('TOKEN')
MAX_LIMIT = float(os.getenv('MAX_LIMIT'))
LAT_FROM = float(os.getenv('LAT_FROM'))
LON_FROM = float(os.getenv('LON_FROM'))
LAT_TO = float(os.getenv('LAT_TO'))
LON_TO = float(os.getenv('LON_TO'))
NOTIFY_ITERATIONS = 6


def main(update: Update, context: CallbackContext) -> None:
    iteration = 0
    while True:
        response = requests.post(
            url='https://taxi.yandex.kz/3.0/routestats',
            headers={
                'Content-Type': 'application/json'
            },
            data=json.dumps({
                "id":POST_ID,
                "zone_name":"almaty",
                "skip_estimated_waiting":True,
                "supports_forced_surge":True,
                "format_currency":True,
                "extended_description":True,
                "route":[[LON_FROM,LAT_FROM],[LON_TO,LAT_TO]],
                "requirements":{}
            })
        )
        yandex_data = response.json()
        price = float(yandex_data.get('service_levels')[0].get('description').split()[1])
        if price <= MAX_LIMIT:
            update.message.reply_text(f'Price has lowered!\nPrice: {price}')
        elif iteration == NOTIFY_ITERATIONS:
            update.message.reply_text(f'Price is still high!\nPrice: {price}')
            iteration = -1
        iteration += 1
        time.sleep(10)


if __name__=='__main__':
    updater = Updater(TOKEN)
    updater.dispatcher.add_handler(CommandHandler('start', main))
    updater.dispatcher.add_handler(CommandHandler('stop', stop))
    updater.start_polling()
    updater.idle()