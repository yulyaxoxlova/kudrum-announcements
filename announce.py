import urllib.request, json, os
from datetime import date, timedelta

today = date.today()
iso_week = today.isocalendar()[1]
monday = today - timedelta(days=today.weekday())
wednesday = monday + timedelta(days=2)
friday = monday + timedelta(days=4)
saturday = monday + timedelta(days=5)

wed_topic = 'Женский Круг' if iso_week % 2 == 1 else 'Книжный Клуб'
sat_topic = 'Творческое занятие' if iso_week % 2 == 0 else 'Разговоры на кухне'
sat_time = '12:10' if iso_week % 2 == 0 else '17:00'
cover_num = ((iso_week - 1) % 5) + 1

caption = (
    'Анонс на неделю ' + monday.strftime('%d.%m') + ' — ' + saturday.strftime('%d.%m') + '\n\n'
    + wed_topic + '\n'
    + 'Среда, ' + wednesday.strftime('%d.%m') + ', 14:30\n\n'
    + 'Индивидуальные консультации\n'
    + 'Пятница, ' + friday.strftime('%d.%m') + ' — по предварительной договорённости\n\n'
    + sat_topic + '\n'
    + 'Суббота, ' + saturday.strftime('%d.%m') + ', ' + sat_time + '\n\n'
    + 'Кудрово, ул. Набережная 8 (кудрУМ)'
)

print('Неделя ' + str(iso_week) + ', обложка cover' + str(cover_num))
print(caption)

token = os.environ['TELEGRAM_BOT_TOKEN']
channel_id = os.environ['TELEGRAM_CHANNEL_ID']

with open('cover' + str(cover_num) + '.jpg', 'rb') as f:
    photo_bytes = f.read()

boundary = '----TgBoundary'
body = (
    '--' + boundary + '\r\nContent-Disposition: form-data; name="chat_id"\r\n\r\n' + channel_id + '\r\n'
    + '--' + boundary + '\r\nContent-Disposition: form-data; name="caption"\r\n\r\n'
).encode('utf-8') + caption.encode('utf-8') + (
    '\r\n--' + boundary + '\r\nContent-Disposition: form-data; name="photo"; filename="cover.jpg"\r\nContent-Type: image/jpeg\r\n\r\n'
).encode('utf-8') + photo_bytes + ('\r\n--' + boundary + '--\r\n').encode('utf-8')

req = urllib.request.Request(
    'https://api.telegram.org/bot' + token + '/sendPhoto',
    data=body,
    headers={'Content-Type': 'multipart/form-data; boundary=' + boundary}
)
resp = urllib.request.urlopen(req)
result = json.loads(resp.read())
print('OK, message_id: ' + str(result['result']['message_id']))
