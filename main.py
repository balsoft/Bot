# Our bot

import time
import datetime
from string import punctuation
import json
import pymorphy2


def rate(a, b):
    return len(list(filter(lambda x: x in b, a))) / len(b)


def parse_times(times_unparsed, time):
    return list(map(lambda x: [x] + list(
        map(lambda y: time.strptime(y, "%H:%M").replace(year=time.year, month=time.month, day=time.day),
            times_unparsed[x].split('-'))),
                    times_unparsed.keys()))


def next_trip(times):
    time = datetime.datetime.now();
    times = list(
        map(lambda y: (y, time.strptime(y, "%H:%M").replace(year=time.year, month=time.month, day=time.day)), times))
    times.sort(key=lambda x: x[1])
    for i in range(len(times) - 1):
        if times[i][1] < time < times[i + 1][1]:
            return times[i + 1]


def event_at(time):
    times = parse_times(actions[action][potok], time)
    for i in times:
        if len(i) == 3:
            if i[1] < time < i[2]:
                yield i


def next_event(time):
    times = parse_times(actions[action][potok], time)
    times.sort(key=lambda x: x[1])
    for i in range(0, len(times) - 1):
        if times[i][1] < time < times[i + 1][1]:
            return times[i + 1][0]


potok = 0

ma = pymorphy2.MorphAnalyzer()

stopwords = json.load(open("stopwords.json"))

place_names = ["лк", "гк", "кпм", "общага", "столовый"]

keywords = json.load(open("keywords.json"))

actions = {
    "places": json.load(open("places.json")),
    "shop": json.load(open("shop.json")),
    "schedule-when": json.load(open("schedule-when.json")),
    "schedule-what-now": json.load(open("schedule-what.json")),
    "schedule-what-at": json.load(open("schedule-what.json")),
    "wifi": json.load(open("wifi.json"))
}

question = input()

question_parsed = list(
    map(lambda x: ma.parse(x)[0].normal_form,
        filter(lambda x: x not in stopwords,
               "".join(map(lambda y: '' if y in punctuation else y, question)).split())))

if max(list(map(lambda x: rate(question_parsed, keywords[x]), keywords))) == 0:
    print("Я не знаю, чем помочь.")
    exit(1)
action = max(keywords, key=lambda x: rate(question_parsed, keywords[x]))
if action == "shop":
    cur_date = datetime.datetime.now().strftime("%d.%m")
    if cur_date in actions[action]:
        print("В магазин сегодня идут отряды ", " ".join(map(str, actions[action][cur_date])))
    else:
        print("Сегодня никто не идет в магазин")
elif action == "schedule-when":
    if max(map(lambda x: rate(question_parsed, actions[action][potok][x]), actions[action][potok])) < 0.1:
        print("Я не знаю, что это")
        exit(1)
    print(max(actions[action][potok], key=lambda x: rate(question_parsed, actions[action][potok][x])))

elif action == "schedule-what-now":
    print("Сейчас ", end="")
    events = list(event_at(datetime.datetime.now()))
    if len(events) == 0:
        print("ничего", end="")
    for i in events:
        print(i[0], end=" ")
    print(", дальше ", end="")
    next_t = next_event(datetime.datetime.now())
    if next_t is None:
        print("ничего")
    else:
        print(next_t)

elif action == "places":
    f = list(filter(lambda x: x in place_names, question_parsed))
    print("Вы можете попасть из", f[0], "в", f[1], "в", next_trip(actions[action][f[0]][f[1]])[0])

