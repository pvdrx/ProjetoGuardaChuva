import sched
import requests
import time

OW_endpoint = "https://api.openweathermap.org/data/2.5/onecall"  # using the 2.5 version but the 3.0 is already out
#  but because im using the free version of the Open Weather api there's a limit on the number of api keys, if you
# want you can create an account and use the 3.0

LAT = "-23.550028"  # new orleans lat because is raining, change to your location after
LONG = "-46.632265"  # new orleans lat because is raining, change to your location after
KEY = "d2273b8b80f906c4070424244d34c785"  # put your api key here

params = {   # feeding the open weather api with the required parameters and excluding necessary data
    "lat": LAT,
    "lon": LONG,
    "appid": KEY,
    "exclude": "daily,minutely,alerts,current"
}
response = requests.get(url=OW_endpoint, params=params)
response.raise_for_status()  # if the api request fail, will raise a issue

data = response.json()   # transforming everything in a json
hours = []


def telegram_bot_send_text(bot_message):

    bot_token = "5537176801:AAHie2D08fR8C6lUkk6Huc899VVW5vN5IcQ"
    bot_chat_id = "5472920233"
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chat_id + '&parse_mode=Markdown&text=' + bot_message

    response_bot = requests.get(send_text)

    return response_bot.json()


rain = False
for x in range(0, 12):  # looping from 0 to 12 to get 12 hours of "work" so the bot run everyday at 7 am to 7pm
    hours.append(data["hourly"][x])
    if hours[x]["weather"][0]["id"] < 700:  # ids lower than 700 mens some type of rain, look at the documentation for
        rain = True  # details https://openweathermap.org/weather-conditions#Weather-Condition-Codes-2

if rain:
    bot_telegram = telegram_bot_send_text("today it will rain, bring an umbrella with you")
    print(bot_telegram)
else:
    sem_chuva = telegram_bot_send_text("it won't rain today")
    print(sem_chuva)
