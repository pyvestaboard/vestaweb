from ninja import Router
from .models import VestaBoard, VestaMessage

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

router = Router()


@router.get('/boards')
def list_boards(request):
	return [
		{"id": board.id, "ip": board.ip}
		for board in VestaBoard.objects.all()
	]

@router.get('/message')
def get_current_message(request):
	return [
		{"message": "current message"}
	]

@router.post('/format_message')
def format_message(request, message: str, vertical_alignment: str, horizontal_alignment: str):
	encoded_message = VestaMessage.format_message(message, vertical_alignment, horizontal_alignment)
	return [
		{"encoded_message": encoded_message}
	]

@router.post('/relay')
def relay_message(request, message: str):
	async_to_sync(update_channel)(message)
	return {
		"message": message
	}
	
async def update_channel(message):
	channel_layer = get_channel_layer()
	if channel_layer:
		await channel_layer.group_send(
			"echo",
			{'type': 'vestaboard_message', 'message': message},
		)