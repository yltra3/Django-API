from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import decorators, status
from rest_framework.response import Response
from .models import DataBase
from requests.auth import HTTPBasicAuth
import requests
import json


@decorators.api_view(["GET"])
def first(request):
    response = requests.get('http://yarlikvid.ru:9999/api/top-secret-data')
    aList = json.loads(response.text)
    i = 0
    # while i != len(aList):  # У меня лапки
    DataBase.objects.create(encrypted_text=aList[i])
    # print(DataBase.objects.values("encrypted_text"))
    # for e in DataBase.objects.all():
    #     print(e.id)

    # for i in base.execute("SELECT * FROM sqlitedb_test"):
    #     print(i)
    return Response(aList, status.HTTP_201_CREATED)


@decorators.api_view(["POST"])
def second(request):

    encrypt = DataBase.objects.encrypted_text
    lst = list(range(len(encrypt)))
    i = 0
    print(lst)
    while i < len(encrypt):
        lst[i] = encrypt[i][0]
        i += 1
    j_data = json.dumps(lst)
    post = requests.post('http://yarlikvid.ru:9999/api/decrypt', auth=HTTPBasicAuth('qummy', 'GiVEmYsecReT!'),
                         data=j_data)
    decrypt = post.text
    decrypt = decrypt.split('","')
    decrypt[0] = decrypt[0].replace('["', '')
    decrypt[len(decrypt)-1] = decrypt[len(decrypt)-1].replace('"]', '') #Привожу список к нужному виду
    i = 0
    while i < len(decrypt):  # Всё ещё лапки
        DataBase.objects.create(decrypted_text=decrypt[i])
        i += 1
    # for j in base.execute("SELECT * FROM sqlitedb_test"):
    #     print(j)
    return Response(decrypt, status.HTTP_201_CREATED)



