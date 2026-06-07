import requests
import os
from dotenv import load_dotenv

load_dotenv()

chat_threads = {}
from datetime import datetime
from dateutil import parser
import telebot
import datetime
from telebot import types
from pprint import pprint
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

#events = []
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
calendar_id = os.getenv('CALENDAR_ID')
calendar_work_id = os.getenv('CALENDAR_WORK_ID')

TOKEN = os.getenv('TELEGRAM_TOKEN')
SHOW = {
    'hbm':'Обитаемая Луна',
    'cu':'Разноцветная вселенная',
    'jtss':'Путешествие по солнечной системе',
    'potu':'Призрак вселенной',
    'was':'Мы все Звёзды',
    'bope':'Рождение планеты земля',
    'gs':'Путеводные звёзды',
    'swwinter':'Времена года: Зима',
    'lq':'Загадка жизни',
    'moe':'Движение земли',
    'sim':'Небо в движении',
    'swspring':'Времена года: Весна',
    'bts':'Экзопланеты',
    'dino': 'Динозавры'
}

class GoogleCalendar:
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    calendar_id = os.getenv('CALENDAR_ID')
    calendar_work_id = os.getenv('CALENDAR_WORK_ID')
    time_now = datetime.datetime.now()
    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(filename=os.getenv('GOOGLE_CREDENTIALS_FILE'), scopes=self.SCOPES)
        self.service = build('calendar', 'v3', credentials=credentials)


def time_parse_format_str(time):
    time_parse = parser.parse(time)
    real_time_start= (datetime.datetime(time_parse.year, time_parse.month, time_parse.day, time_parse.hour+3, time_parse.minute))
    real_time_str = real_time_start.strftime('%H:%M')
    return real_time_str

def get_worker_today():
    while True:
        worker = []
        time_now = datetime.datetime.now()
        start = (datetime.datetime(time_now.year, time_now.month, time_now.day, 0, 0)).isoformat() + 'Z'
        tomorrow = time_now + datetime.timedelta(days=1)
        end = (datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 0)).isoformat() + 'Z'
        events = obj.service.events().list(calendarId=calendar_work_id, timeMin=start, timeMax=end, singleEvents=True, orderBy='startTime', maxResults=10, timeZone="UTC").execute()
        for event in events['items']:
            worker.append(event['summary'])
        if worker:
            names = '\n'.join(worker)
            return f'Сегодня в БЗЗ:\n{names}'
        else:
            return 'Сегодня в БЗЗ: нет данных в календаре'

def get_today_events_from_google():
    page_token = ''
    list_event = []
    try:
        time_now = datetime.datetime.now();
        start = (datetime.datetime(time_now.year, time_now.month, time_now.day, time_now.hour, time_now.minute)).isoformat() + 'Z'
        tomorrow = time_now + datetime.timedelta(days=1)
        end =  (datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 00, 00)).isoformat() + 'Z'
        events = obj.service.events().list(calendarId=calendar_id, timeMin=start, timeMax=end, singleEvents=True, orderBy='startTime', maxResults=10, timeZone="UTC").execute()
        while True:
            for event in events['items']:
                event_name = event['summary']
                event_start_time = event['start']['dateTime']
                event_end_time = event['end']['dateTime']
                real_time_est_str = time_parse_format_str(event_start_time)
                real_time_eet_str = time_parse_format_str(event_end_time)
                all_time = f'{real_time_est_str}-{real_time_eet_str}'
                list_event.append(f'{all_time} : {event_name}')
            if not page_token:
                break
            if not events['items']:
                print('No upcoming events found.')
                return 'Сегодня шоу больше нет'
        return list_event

    except HttpError as error:
        print('An error occurred: %s' % error)

def get_data_from_google():
    page_token = ''
    try:
        time_now = datetime.datetime.now();
        start = (datetime.datetime(time_now.year, time_now.month, time_now.day, time_now.hour, time_now.minute)).isoformat() + 'Z'
        time_now_correct = (datetime.datetime(time_now.year, time_now.month, time_now.day, time_now.hour+3, time_now.minute))
        tomorrow = time_now + datetime.timedelta(days=1)
        end =  (datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 00, 00)).isoformat() + 'Z'
        events = obj.service.events().list(calendarId=calendar_id, timeMin=start, timeMax=end, singleEvents=True, orderBy='startTime', maxResults=2, timeZone="UTC").execute()
        while True:
            for event in events['items']:
                event_name = event['summary']
                event_start_time = event['start']['dateTime']
                d = parser.parse(event_start_time)
                real_time = (datetime.datetime(d.year, d.month, d.day, d.hour+3, d.minute))
                real_time_str = real_time.strftime('%H:%M')
                if real_time > time_now_correct:
                    print(f'{real_time} > {time_now}')
                    print(event['summary'], event['start']['dateTime'])
                    return f'{event_name}\nНачало в {real_time_str}'
                page_token = event.get('nextPageToken')
            if not page_token:
                break
            if not events['items']:
                print('No upcoming events found.')
                return 'Сегодня шоу больше нет'

    except HttpError as error:
        print('An error occurred: %s' % error)

def get_data():
    req = requests.get("https://91.229.###.###/api/narrations")
    response = req.json()
    sell_price = response["show_name"]["end_time_ms"]


def make_inline_markup():
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("🎬 Show", callback_data="show"),
        types.InlineKeyboardButton("📅 Today", callback_data="today")
    )
    markup.row(
        types.InlineKeyboardButton("👤 Employee", callback_data="employee"),
        types.InlineKeyboardButton("📋 BusyBoard", callback_data="busyboard")
    )
    markup.row(
        types.InlineKeyboardButton("🎭 Малый зал", callback_data="mzz"),
        types.InlineKeyboardButton("🎬 4D-кинотеатр", callback_data="4d")
    )
    return markup

def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=["start"])
    def start_message(message):
        if message.message_thread_id:
            chat_threads[message.chat.id] = message.message_thread_id
        bot.send_message(
            message.chat.id,
            "Добро пожаловать в бот сервис БЗЗ.",
            reply_markup=make_inline_markup(),
            message_thread_id=chat_threads.get(message.chat.id)
        )

    @bot.message_handler()
    def send_text(message):
        if message.message_thread_id:
            chat_threads[message.chat.id] = message.message_thread_id
        if message.text and message.text.lower() == "бот":
            bot.send_message(
                message.chat.id,
                "Слушаю!",
                reply_markup=make_inline_markup(),
                message_thread_id=chat_threads.get(message.chat.id)
            )

    @bot.callback_query_handler(func=lambda call: True)
    def handle_callback(call):
        bot.answer_callback_query(call.id)
        time = datetime.datetime.now()
        real_time = (datetime.datetime(time.year, time.month, time.day, time.hour+3, time.minute))
        real_time_str = real_time.strftime('%H:%M')
        thread_id = chat_threads.get(call.message.chat.id)
        if call.data == "show":
            try:
                loading = bot.send_message(call.message.chat.id, "⏳ Загружаю...", message_thread_id=thread_id)
                time_now = datetime.datetime.now()
                start = (datetime.datetime(time_now.year, time_now.month, time_now.day, 0, 0)).isoformat() + 'Z'
                tomorrow = time_now + datetime.timedelta(days=1)
                end = (datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 0)).isoformat() + 'Z'
                events = obj.service.events().list(calendarId=calendar_id, timeMin=start, timeMax=end, singleEvents=True, orderBy='startTime', maxResults=20, timeZone="UTC").execute()
                items = events.get('items', [])
                current_show = None
                next_show = None
                for event in items:
                    ev_start = datetime.datetime.fromisoformat(event['start'].get('dateTime', '').replace('Z',''))
                    ev_end = datetime.datetime.fromisoformat(event['end'].get('dateTime', '').replace('Z',''))
                    ev_start_msk = ev_start + datetime.timedelta(hours=3)
                    ev_end_msk = ev_end + datetime.timedelta(hours=3)
                    real_now = datetime.datetime.now() + datetime.timedelta(hours=3)
                    if ev_start_msk <= real_now <= ev_end_msk:
                        current_show = (event.get('summary','—'), ev_end_msk.strftime('%H:%M'))
                    elif ev_start_msk > real_now and next_show is None:
                        next_show = (event.get('summary','—'), ev_start_msk.strftime('%H:%M'))
                if current_show:
                    msg = f"Текущее время: {real_time_str}\n\n🎬 Идёт сеанс: {current_show[0]}\nОкончание: {current_show[1]}"
                    if next_show:
                        msg += f"\n\n⏭ Следующий: {next_show[0]} в {next_show[1]}"
                    else:
                        msg += "\n\nНа сегодня всё!"
                else:
                    if next_show:
                        msg = f"Текущее время: {real_time_str}\n\nВ БЗЗ перерыв.\n\n⏭ Следующий сеанс: {next_show[0]} в {next_show[1]}"
                    else:
                        msg = f"Текущее время: {real_time_str}\n\nНа сегодня всё!"
                bot.edit_message_text(msg, call.message.chat.id, loading.message_id)
            except Exception as ex:
                print(ex)
                bot.edit_message_text("Упс... Что-то пошло не так...", call.message.chat.id, loading.message_id)
        elif call.data == "today":
            result = get_today_events_from_google()
            results = "\n".join(result)
            bot.send_message(
                call.message.chat.id,
                f"Текущее время: {real_time_str}\n\n{results}",
                message_thread_id=thread_id
            )
        elif call.data == "employee":
            bot.send_message(
                call.message.chat.id,
                f"{get_worker_today()}",
                message_thread_id=thread_id
            )
        elif call.data == "mzz":
            try:
                time_now = datetime.datetime.now()
                real_now = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None) + datetime.timedelta(hours=3)
                start = (datetime.datetime(time_now.year, time_now.month, time_now.day, 0, 0)).isoformat() + 'Z'
                tomorrow = time_now + datetime.timedelta(days=1)
                end = (datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 0)).isoformat() + 'Z'
                events = obj.service.events().list(calendarId=os.getenv('CALENDAR_MZZ_ID'), timeMin=start, timeMax=end, singleEvents=True, orderBy='startTime', maxResults=20, timeZone="UTC").execute()
                items = events.get('items', [])
                if items:
                    lines = []
                    has_future = False
                    for event in items:
                        summary = event.get('summary', '—')
                        start_time = event['start'].get('dateTime', event['start'].get('date', ''))
                        if 'T' in start_time:
                            dt = datetime.datetime.fromisoformat(start_time)
                            dt_msk = dt + datetime.timedelta(hours=3)
                            end_time = event['end'].get('dateTime', '')
                            dt_end = datetime.datetime.fromisoformat(end_time).replace(tzinfo=None) + datetime.timedelta(hours=3)
                            if dt_end > real_now:
                                has_future = True
                            lines.append(f"{dt_msk.strftime('%H:%M')} — {summary}")
                        else:
                            lines.append(f"Весь день — {summary}")
                            has_future = True
                    if has_future:
                        result = '\n'.join(lines)
                        bot.send_message(call.message.chat.id, f"🎭 Малый зал на сегодня:\n\n{result}", message_thread_id=thread_id)
                    else:
                        bot.send_message(call.message.chat.id, "Малый зал закончил работу.", message_thread_id=thread_id)
                else:
                    bot.send_message(call.message.chat.id, "Малый зал закончил работу.", message_thread_id=thread_id)
            except Exception as ex:
                import traceback
                print(f"ERROR: {ex}")
                traceback.print_exc()
                bot.send_message(call.message.chat.id, "Упс... Что-то пошло не так...", message_thread_id=thread_id)
        elif call.data == "4d":
            try:
                time_now = datetime.datetime.now()
                real_now = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None) + datetime.timedelta(hours=3)
                start = (datetime.datetime(time_now.year, time_now.month, time_now.day, 0, 0)).isoformat() + 'Z'
                tomorrow = time_now + datetime.timedelta(days=1)
                end = (datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 0)).isoformat() + 'Z'
                events = obj.service.events().list(calendarId=os.getenv('CALENDAR_4D_ID'), timeMin=start, timeMax=end, singleEvents=True, orderBy='startTime', maxResults=20, timeZone="UTC").execute()
                items = events.get('items', [])
                if items:
                    lines = []
                    has_future = False
                    for event in items:
                        summary = event.get('summary', '—')
                        start_time = event['start'].get('dateTime', event['start'].get('date', ''))
                        if 'T' in start_time:
                            dt = datetime.datetime.fromisoformat(start_time)
                            dt_msk = dt + datetime.timedelta(hours=3)
                            end_time = event['end'].get('dateTime', '')
                            dt_end = datetime.datetime.fromisoformat(end_time).replace(tzinfo=None) + datetime.timedelta(hours=3)
                            if dt_end > real_now:
                                has_future = True
                            lines.append(f"{dt_msk.strftime('%H:%M')} — {summary}")
                        else:
                            lines.append(f"Весь день — {summary}")
                            has_future = True
                    if has_future:
                        result = '\n'.join(lines)
                        bot.send_message(call.message.chat.id, f"🎬 4D-кинотеатр на сегодня:\n\n{result}", message_thread_id=thread_id)
                    else:
                        bot.send_message(call.message.chat.id, "Кинотеатр завершил работу.", message_thread_id=thread_id)
                else:
                    bot.send_message(call.message.chat.id, "Кинотеатр завершил работу.", message_thread_id=thread_id)
            except Exception as ex:
                import traceback
                print(f"ERROR: {ex}")
                traceback.print_exc()
                bot.send_message(call.message.chat.id, "Упс... Что-то пошло не так...", message_thread_id=thread_id)
        elif call.data == "busyboard":
            try:
                time_now = datetime.datetime.now()
                start = (datetime.datetime(time_now.year, time_now.month, time_now.day, 0, 0)).isoformat() + 'Z'
                tomorrow = time_now + datetime.timedelta(days=1)
                end = (datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 0)).isoformat() + 'Z'
                events = obj.service.events().list(calendarId=os.getenv('CALENDAR_BUSY_ID'), timeMin=start, timeMax=end, singleEvents=True, orderBy='startTime', maxResults=20, timeZone="UTC").execute()
                items = events.get('items', [])
                if items:
                    lines = []
                    for event in items:
                        summary = event.get('summary', '—')
                        start_time = event['start'].get('dateTime', event['start'].get('date', ''))
                        if 'T' in start_time:
                            dt = datetime.datetime.fromisoformat(start_time)
                            dt = dt + datetime.timedelta(hours=3)
                            time_str = dt.strftime('%H:%M')
                            lines.append(f"{time_str} — {summary}")
                        else:
                            lines.append(f"Весь день — {summary}")
                    result = '\n'.join(lines)
                    bot.send_message(call.message.chat.id, f"📋 План на сегодня:\n\n{result}", message_thread_id=thread_id)
                else:
                    bot.send_message(call.message.chat.id, "На сегодня событий нет.", message_thread_id=thread_id)
            except Exception as ex:
                import traceback
                print(f"ERROR: {ex}")
                traceback.print_exc()
                bot.send_message(call.message.chat.id, "Упс... Что-то пошло не так...", message_thread_id=thread_id)

    while True:
        try:
            bot.polling()
        except:
            continue

if __name__ == '__main__':
    obj = GoogleCalendar()
    telegram_bot(TOKEN)
    
