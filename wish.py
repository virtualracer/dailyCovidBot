import time
import json
import urllib3
import random
import locale
locale.setlocale(locale.LC_ALL, '')

http = urllib3.PoolManager()

# testBot = 1392096396:AAGwZfy5fk0bywDGNYtSolMDYV7MafAGJOY
# covidBot = 1308060193:AAFkI1FAWd5k_Wf7Vk6sSzAgXVCdEg7lIeY

def check_users(token):
    url = f'https://api.telegram.org/bot{token}/getUpdates'
    r = http.request('GET', url)
    dec_resp = json.loads(r.data.decode('utf-8'))
    lenId = len(dec_resp['result'])
    userArr = []
    nameArr = []
    for x in range(0,lenId):
        id = dec_resp['result'][x]['message']['chat']['id']
        name = dec_resp['result'][x]['message']['chat']['first_name']
        userArr.append(id)
        nameArr.append(name)
    userArr = list(dict.fromkeys(userArr))
    nameArr = list(dict.fromkeys(nameArr))
    return userArr, nameArr

def send_wish(msg, userList, nameList, token):
    userList = userList
    nameList = nameList
    listLen = len(userList)
    for x in range(0, listLen):
        send_text = 'https://api.telegram.org/bot' + token + \
        '/sendMessage?chat_id=' + str(userList[x]) + '&parse_mode=markdown&text=*Good Morning ' + str(nameList[x]) + '!*' + msg
        response = http.request('GET', send_text)


def get_covid_data():
    url = 'https://api.covid19india.org/data.json'
    r = http.request('GET', url)
    dec_resp = json.loads(r.data.decode('utf-8'))
    total_confirmed = int(dec_resp['statewise'][0]['confirmed'])
    total_active = int(dec_resp['statewise'][0]['active'])
    total_recovered = int(dec_resp['statewise'][0]['recovered'])
    total_deaths = int(dec_resp['statewise'][0]['deaths'])

    daily_confirmed = int(dec_resp['cases_time_series'][-1]['dailyconfirmed'])
    daily_deceased = int(dec_resp['cases_time_series'][-1]['dailydeceased'])
    daily_recovered = int(dec_resp['cases_time_series'][-1]['dailyrecovered'])

    msg = f"CoViD Updates:\n" \
          f"Yesterday Confirmed: *{daily_confirmed:n}*\nYesterday Recovered: *{daily_recovered:n}*\nYesterday Deceased: *{daily_deceased:n}*\n-----------------------------------------\n" \
          f"Total Confirmed: *{total_confirmed:n}*\nTotal Active: *{total_active:n}*\nTotal Recovered: *{total_recovered:n}*\nTotal Deaths: *{total_deaths:n}*" \
          f"\n\n*Stay Home, Stay Safe* \U0001f9e1"
    return msg


def get_quote():
    url = 'https://type.fit/api/quotes'
    r = http.request('GET', url)
    dec_resp = json.loads(r.data.decode('utf-8'))
    rand = random.randint(0, 1600)
    quote = dec_resp[rand]['text']
    author = dec_resp[rand]['author']

    msg = f"\n\n*{quote}*\n~ {author}\n\n"
    return msg


def create_wish():
    token = '1392096396:AAGwZfy5fk0bywDGNYtSolMDYV7MafAGJOY'
    quote = get_quote()
    covid = get_covid_data()
    userList, nameList = check_users(token)
    msg = f'{quote}{covid}'
    send_wish(msg, userList, nameList, token)


create_wish()


