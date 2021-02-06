import time
from ast import literal_eval

from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from screencontrol.models import Client
from screencontrol.capture import VideoFeed
from screencontrol.user_input import UserInput
from WebTop import settings


def loop(feed):
    while True:
        start_time = time.time()
        frame = feed.get_frame()
        yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'
        time.sleep(max(1. / 30 - (time.time() - start_time), 0))


def index(request):
    client_ip = request.META.get('REMOTE_ADDR')
    client, _ = Client.objects.get_or_create(ip_address=client_ip)

    if client.allowed_control:
        return render(request, 'screencontrol/webtop.html')
    else:
        return HttpResponse('You are not allowed to control yet.')


@csrf_exempt
def postkeys(request):
    # GET, POST
    rep = literal_eval(str(request.body).split("\'")[1])
    ui = UserInput()
    ui.keys = rep["keys"]
    ui.mouse = rep["mouse"]
    ui.click = rep["click"]
    ui.start()
    return HttpResponse()


@csrf_exempt
def size(request):
    # GET, POST
    rep = literal_eval(str(request.body).split("\'")[1])
    settings.TARGET_WIDTH = rep["width"]
    settings.TARGET_HEIGHT = rep["height"]
    return HttpResponse()


def video_feed(request):
    return StreamingHttpResponse(loop(VideoFeed()), content_type='multipart/x-mixed-replace; boundary=frame')
