from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

from .models import VestaBoard, VestaMessage


def index(request):
	template = loader.get_template("vestaboard/index.html")
	context = {"vestaboard": VestaBoard.objects.first()}
	return HttpResponse(template.render(context, request))

def message(request):
    template = loader.get_template("vestaboard/message.html")
    context = {"message": VestaBoard.objects.first().get_message()}
    return HttpResponse(template.render(context, request))