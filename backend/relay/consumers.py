import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer


class EchoConsumer(JsonWebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)("echo", self.channel_name)
        self.accept()
    
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("echo", self.channel_name)
        
    def receive_json(self, content):
        async_to_sync(self.channel_layer.group_send)(
            "echo",
            {
                "type": "vestaboard.message",
            } | content,
        )

    def vestaboard_message(self, event):
        self.send_json(event)