from django.shortcuts import render
from django.http import JsonResponse
from agora_token_builder import RtcTokenBuilder
import random
import time
import json

from .models import RoomMember

from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def getToken(request):
    appId = "b3ef1102093348b6bf9c4c67fee4c442"
    appCertificate = "0d3f969148144ac698b994237d4910a9"
    channelname = request.GET.get("channel")
    uid = random.randint(1, 230)
    expiration_time_in_seconds = 3600 * 24
    current_time_stamp = time.time()
    privilege_expired_token = current_time_stamp + expiration_time_in_seconds
    role = 1
    token = RtcTokenBuilder.buildTokenWithUid(
        appId=appId,
        appCertificate=appCertificate,
        channelName=channelname,
        uid=uid,
        role=role,
        privilegeExpiredTs=privilege_expired_token,
    )
    return JsonResponse({"token": token, "uid": uid}, safe=False)


def lobby(request):
    return render(request, "base/lobby.html")


def room(request):
    return render(request, "base/room.html")


@csrf_exempt
def createUser(request):
    data = json.loads(request.body)

    member, created = RoomMember.objects.get_or_create(
        name=data["name"], uid=data["UID"], room_name=data["room_name"]
    )
    return JsonResponse({"name": data["name"]}, safe=False)


def getMember(request):
    uid = request.GET.get("uid")
    room_name = request.GET.get("room_name")

    member = RoomMember.objects.get(uid=uid, room_name=room_name)

    name = member.name
    return JsonResponse({"name": name}, safe=False)


@csrf_exempt
def deleteUser(request):
    data = json.loads(request.body)

    member = RoomMember.objects.get(
        uid=data["UID"], room_name=data["room_name"], name=data["name"]
    ).delete()
    return JsonResponse("Member was deleted", safe=False)
