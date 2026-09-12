from ninja import Router, Schema, Status, NinjaAPI
from .models import VestaBoard, VestaMessage

from pydantic import field_validator

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from pyvestaboard import VestaBoard as PyVestaBoard


class Message(Schema):
	message: str

class RelayMessage(Schema):
	message: str
	vertical_alignment: str
	horizontal_alignment: str
	
	@field_validator("vertical_alignment")
	def vertical_alignment_validator(cls, value: str) -> str:
		print("Asdf")
		if value not in PyVestaBoard.VERTICAL_ALIGN_OPTIONS:
			raise ValueError(f"vertical alignment needs to be one of {PyVestaBoard.VERTICAL_ALIGN_OPTIONS}")
		return value

api = NinjaAPI()
router = Router()

@api.exception_handler(ValueError)
def value_error(request, exc):
	import ipdb; ipdb.set_trace()
	return response.create_response(
		request,
		{"message": "Please retry later"},
		status=400,
	)

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

@router.post('/relay', response={200: Message, 400: Message})
def relay_message(request, data: RelayMessage):
	# if data.vertical_alignment not in PyVestaBoard.VERTICAL_ALIGN_OPTIONS:
	# 	return Status(400, {"message": "asdf"})
	# 	return 400, {
	# 		"message": f"vertical alignment needs to be one of {PyVestaBoard.VERTICAL_ALIGN_OPTIONS}",
	# 		"code": 400,
	# 	}
	async_to_sync(update_channel)(data.message, data.vertical_alignment, data.horizontal_alignment)
	return {
		"message": data.message
	}
	
async def update_channel(message, vertical_alignment, horizontal_alignment):
	channel_layer = get_channel_layer()
	if channel_layer:
		await channel_layer.group_send(
			"echo",
			{
				'type': 'vestaboard_message',
				'message': message,
				'vertical_alignment': vertical_alignment,
				'horizontal_alignment': horizontal_alignment,
			},
		)

router.api = api
api.add_router("/relay", router)