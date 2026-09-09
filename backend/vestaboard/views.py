from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

from .models import VestaBoard, VestaMessage
from pyvestaboard import VestaBoard as PyVestaBoard, VestaCodes, CommunicationException

def index(request):
	template = loader.get_template("vestaboard/index.html")
	context = {"vestaboard": VestaBoard.objects.first()}
	return HttpResponse(template.render(context, request))

def message(request):
    template = loader.get_template("vestaboard/message.html")
    context = {"message": VestaBoard.objects.first().get_encoded_message()}
    return HttpResponse(template.render(context, request))

def current_message(request):
	encoded_message = VestaBoard.objects.first().get_encoded_message()
	message = ""
	for row in encoded_message:
		message_row = "".join(row).strip()
		message += f"{message_row}<br>"
	return HttpResponse(message)

def _message(message, horizontal_alignment, vertical_alignment):
	raw_message = PyVestaBoard.format_message(
		message, vertical_alignment, horizontal_alignment
	)
	decoded_message = PyVestaBoard.blank_message()
	for i, row in enumerate(raw_message):
		for j, code in enumerate(row):
			decoded_message[i][j] = VestaCodes.from_code(code)
	return decoded_message

def preview_message(request):
	message = request.POST['message']
	horizontal_alignment = request.POST['horizontal-alignment']
	vertical_alignment = request.POST['vertical-alignment']
	
	decoded_message = _message(message, horizontal_alignment, vertical_alignment)
	template = loader.get_template("vestaboard/message.html")
	return HttpResponse(template.render({"message": decoded_message}, request))

def send_message(request):
	message = request.POST['message']
	horizontal_alignment = request.POST['horizontal-alignment']
	vertical_alignment = request.POST['vertical-alignment']
	board = VestaBoard.objects.first()
	board.send_message(message, vertical_alignment, horizontal_alignment)
	
	return preview_message(request)
