from ninja import Router
from .models import VestaBoard, VestaMessage

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
def format_message(message: str, vertical_alignment: str, horizontal_alignment: str):
	encoded_message = VestaMessage.format_message(message, vertical_alignment, horizontal_alignment)
	return [
		{"encoded_message": encoded_message}
	]