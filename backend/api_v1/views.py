from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from pyvestaboard import VestaBoard as PyVestaBoard

from backend.vestaboard.models import VestaBoard, VestaMessage

from .serializers import RelayMessageSerializer


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

class RelayMessageView(APIView):
	serializer_class = RelayMessageSerializer

	def post(self, request):
		serializer = RelayMessageSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		async_to_sync(update_channel)(
			serializer.validated_data['message'],
			serializer.validated_data['vertical_alignment'],
			serializer.validated_data['horizontal_alignment'],
		)
		return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
