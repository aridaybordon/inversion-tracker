import os
import yfinance as yf

from datetime import date
from telegram import ParseMode, Bot

from scripts.database import return_degiro_balance
from scripts.crypto.personal import return_personal_crypto_balance
from scripts.plot import create_weekly_plot

TOKEN, CHAT_ID = os.environ["TOKEN"], os.environ["CHAT_ID"]


def send_daily_report():
    bot = Bot(token=TOKEN)

    today       = date.today().strftime('%d/%m/%Y')
    now, last   = return_degiro_balance(2)
    dif         = (now - last) / last

    crypto      = return_personal_crypto_balance()

    text   = f'<b>Daily report</b> ({today})\n\nYour total DEGIRO account\'s balance is {now:.2f}€ ({dif:+.2%}).'
    text  += f'\nYour crypto addresses balance is {crypto:.2f}'

    bot.send_message(chat_id=CHAT_ID, text=text, parse_mode=ParseMode.HTML)


def send_weekly_report():
    create_weekly_plot()

    bot     = Bot(token=TOKEN)

    week    = date.today().strftime('%U/%Y')
    balance = return_degiro_balance(5)
    dif     = (balance[0] - balance[-1]) / balance[-1]

    text    = f'<b>Weekly report</b> (week {week})\nDuring this week, your investment have yield a total of {dif:+.2%}.'
    bot.send_message(chat_id=CHAT_ID, text=text, parse_mode=ParseMode.HTML)
    bot.send_photo(chat_id=CHAT_ID, photo=open('plots/weekly-report.png', 'rb'))
