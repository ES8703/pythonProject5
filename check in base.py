from aiogram import Bot, executor, Dispatcher
import requests
import time
import schedule
import pymongo
limit_request=7
message_limit=3

client_1 = pymongo.MongoClient("mongodb://localhost:27017/")
db_1 = client_1["added"]
collection_1 = db_1["files_1"]
client_2 = pymongo.MongoClient("mongodb://localhost:27017/")
db_2 = client_2['added_on_message']
collection_2 = db_2['files_2']

seconds = time.time()
t = time.ctime(seconds)
day = t[0:3]
catday = {'Mon': 'sibe', 'Tue': 'aege', 'Wed': 'beng', 'Thu': 'java', 'Fri': 'kora', 'Sat': 'kuri', 'Sun': 'manx'}
breed = catday[day]

token = '?????????????'
bot = Bot(token)
dp = Dispatcher(bot=bot)
groupid=-1001949097641

def cat_collection_generator():#делаю запрос и создаю список из словарей
    seconds = time.time()
    t = time.ctime(seconds)
    day = t[0:3]
    catday = {'Mon': 'sibe', 'Tue': 'aege', 'Wed': 'beng', 'Thu': 'java', 'Fri': 'kora', 'Sat': 'kuri', 'Sun': 'manx'}
    breed = catday[day]
    zapros = f'https://api.thecatapi.com/v1/images/search?limit={limit_request}&breed_ids={breed}&api_key=live_NSO4T9haPU0a9yrI3913IfghtcXGcqlTn7FeMmPDQ72nYMC5fAq5x6pmg9IymUAD'
    response = requests.get(zapros)
    resp = response.json()
    listcats=[]
    lc_check=[]
    for i in resp:
        x=i['url']
        lc_check.append(x)
    for i in resp:
        q={breed:i}
        listcats.append(q)
    return lc_check,listcats#возвращается список из словарей
json_format_request=cat_collection_generator()[1]
list_format_request=cat_collection_generator()[0]

#добавление в базу
#проверка значений в базе
#лист проверки соответствий с базой_1
#Я НАШЁЛ РАБОЧУЮ ПРОВЕРКУ СООТВЕТСТВИЙ В БАЗЕ!!!!!!!!!

####формирование проверки на идентичность в базе
list_format_base=[]
for i in list(collection_1.find()):
    k=tuple(i.values())[1]
    list_format_base.append(k)
for i in list_format_request:
    part_of_json_format_request = {breed: i}
    if i not in list_format_base:
        collection_1.insert_one(part_of_json_format_request)



#НЕ УДАЛЯЙ ЭТУ ЧАСТЬ КОДА,ОНА РАБОТАЕТ,КАК НАДО
#ПОГОВОРИТЬ С СЕРЁГОЙ О ТОМ, ЧТО НА САЙТЕ ТОЛЬКО 8 ВАРИАНТОВ ОДНОЙ ПОРОДЫ

#!!!!!!В БАЗЕ НАХОДЯТСЯ ТОЛЬКО не ПОВТОРЯЮЩИЕСЯ ЭЛЕМЕНТЫ!!!!!!
# ТЕПЕРЬ 1.Формируем сообщение (список из 3х элементов),при условии,что этих элементов нет во 2й базе
#        2.отправляем сообщение и добавляем его содержание во 2ю базу
#list_format_base - переменная в которой база №1 в формате списка



#формирование 2й коллекции в формате списка
list_format_base_2=[]

for i in list(collection_2.find()):
    k=tuple(i.values())[1]
    list_format_base_2.append(k)


### формирование сообщения###
text_message=[]
for i in list_format_base:
    if i not in list_format_base_2 and len(text_message)<message_limit:
        text_message.append(i)


#Нужно отправить сформированное сообщение и добавить его в базу №2


async def send_echo():
    for i in text_message:
        await bot.send_photo(groupid,photo=i)

def xt():
    executor.start(dp,send_echo())

def x():
    schedule.every(3).seconds.do(xt)#могу написать at и любое время
    while True:
        schedule.run_pending()



###добавление в базу 2 плохо работает интернет, научусь заливать на гит,а дальше доделаю код
for i in text_message:
    elem_for_base_2={breed:i}
    collection_2.insert_one(elem_for_base_2)
print(list(collection_2.find()))


#Не работает добавление во 2ю базу и отправка сообщения


