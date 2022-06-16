from django.http import HttpResponse
import requests
import sqlite3
import json
import datetime
import re
#import base64
from requests.auth import HTTPBasicAuth
from os.path import abspath, dirname, join

import django
from django.conf import settings


# SETTINGS
BASE_DIR = dirname(abspath(__file__))
DEBUG = True
ROOT_URLCONF = "mini_django"  # this module
DATABASES = {"default": {}}  # required regardless of actual usage
TEMPLATES = [
    {"BACKEND": "django.template.backends.django.DjangoTemplates", "DIRS": [BASE_DIR,]}
]
STATIC_URL = "/static/"
STATICFILES_DIRS = (join(BASE_DIR, "static"),)
SECRET_KEY = "not so secret",

SETTINGS = dict((key,val) for key, val in locals().items() if key.isupper())
if not settings.configured:
    settings.configure(**SETTINGS)
django.setup()

def first():
    response = requests.get('http://yarlikvid.ru:9999/api/top-secret-data')
    aList = json.loads(response.text)
    try:
        sqlite_connection = sqlite3.connect('sqlite_python.db')
        base = sqlite_connection.cursor()
        base.execute("""DROP TABLE IF EXISTS sqlitedb_test""")
        base.execute("""CREATE TABLE IF NOT EXISTS sqlitedb_test 
        (id TEXT, encrypted_text TEXT, decrypted_text TEXT, created_at TEXT);""")
        sqlite_connection.commit()

        print("База данных создана и успешно подключена к SQLite")
        i = 0
        while i != len(aList): # У меня лапки
            base.execute(f"INSERT INTO sqlitedb_test(id, encrypted_text, created_at) VALUES('{i}', '{aList[i]}', "
                         f"'{datetime.date.today()}')")
            i += 1
        # for i in base.execute("SELECT * FROM sqlitedb_test"):
        #     print(i)
        sqlite_connection.commit()
        base.close()
    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
    return HttpResponse(status=201), aList


def second():
    try:
        sqlite_connection = sqlite3.connect('sqlite_python.db')
        base = sqlite_connection.cursor()

        def get_not_without_paranth(): #по итогу всё равно со скобками, как же долго я эти кортежи мучал
            return [row for row in base.execute("SELECT encrypted_text FROM sqlitedb_test").fetchall()]
        encrypt = get_not_without_paranth()
        lst = list(range(len(encrypt)))
        i = 0
        while i < len(encrypt):
            lst[i] = encrypt[i][0]
            i += 1
        #print(lst)
        # ns = str.join(encrypt[0])
        # print(ns)
        # new_lst = list(range(len(encrypt)))
        # while i < len(encrypt):
        #     new_lst[i] = [*encrypt[i]]
        #     i += 1
        # i = 0
        # while i < len(new_lst):
        #     new_lst[i].replace('[', '')
        #     i += 1
        # print(new_lst)
        j_data = json.dumps(lst)
        #print(j_data)
        #payload = {'data': j_data}
        # b64 = "qummy:GiVEmYsecReT!"
        # enb64 = base64.b64encode(b64.encode('utf-8'))
        # myjson ={
        #         "Authorization": "BASIC cXVtbXk6R2lWRW1Zc2VjUmVUIQ=="
        #         }
        # Я честно замучался с этим вариантом авторизации
        post = requests.post('http://yarlikvid.ru:9999/api/decrypt', auth=HTTPBasicAuth('qummy', 'GiVEmYsecReT!'),
                             data=j_data)
        decrypt = post.text
        decrypt = decrypt.split('","')
        decrypt[0] = decrypt[0].replace('["', '')
        decrypt[len(decrypt)-1] = decrypt[len(decrypt)-1].replace('"]', '') #Привожу список к нужному виду
        i = 0
        while i < len(decrypt):  # Всё ещё лапки
            base.execute(f"UPDATE sqlitedb_test set decrypted_text = '{decrypt[i]}' WHERE id={i}")
            i += 1
        sqlite_connection.commit()
        # for j in base.execute("SELECT * FROM sqlitedb_test"):
        #     print(j)
        base.close()
    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
    return HttpResponse(status=201), decrypt

def third():
    try:
        sqlite_connection = sqlite3.connect('sqlite_python.db')
        base = sqlite_connection.cursor()

        def get_not_without_paranth():
            return [row for row in base.execute("SELECT decrypted_text FROM sqlitedb_test").fetchall()]
        decrypt = get_not_without_paranth()
        lst = list(range(len(decrypt)))
        i = 0
        while i < len(decrypt):
            lst[i] = decrypt[i][0]
            i += 1
        #print(lst)
        j_data = json.dumps(lst)
        #print(j_data)
        myjson = {
                "name": "Михайлюк Владислав",
                "repo_url": "https://github.com/test/test-repo",
                "result": j_data
                 }
        post = requests.post('http://yarlikvid.ru:9999/api/decrypt', auth=HTTPBasicAuth('qummy', 'GiVEmYsecReT!'),
                         data=myjson)
    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
    return HttpResponse(status=201), decrypt

def main():
    second()
    #third()


if __name__ == "__main__":
    main()
