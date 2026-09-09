import requests
import math
import json
import regex

from django.db import models

from pyvestaboard import VestaBoard as PyVestaBoard, CommunicationException, VestaCodes


class VestaMessage(models.Model):
    ANIMATION_CHOICES = [
        (PyVestaBoard.ANIMATION_COLUMN, "Column"),
        (PyVestaBoard.ANIMATION_REVERSE_COLUMN, "Reverse Column"),
        (PyVestaBoard.ANIMATION_EDGES_TO_CENTER, "Edges to Center"),
        (PyVestaBoard.ANIMATION_ROW, "Row"),
        (PyVestaBoard.ANIMATION_DIAGONAL, "Diagonal"),
        (PyVestaBoard.ANIMATION_RANDOM, "Random"),
    ]

    VERTICAL_ALIGN_CHOICES = [
        (PyVestaBoard.VERTICAL_ALIGN_TOP, "Top"),
        (PyVestaBoard.VERTICAL_ALIGN_MIDDLE, "Middle"),
        (PyVestaBoard.VERTICAL_ALIGN_BOTTOM, "Bottom"),
        (PyVestaBoard.VERTICAL_ALIGN_JUSTIFIED, "Justified"),
    ]
    
    HORIZONTAL_ALIGN_CHOICES = [
        (PyVestaBoard.HORIZONTAL_ALIGN_LEFT, "Left"),
        (PyVestaBoard.HORIZONTAL_ALIGN_CENTER, "Center"),
        (PyVestaBoard.HORIZONTAL_ALIGN_RIGHT, "Right"),
        (PyVestaBoard.HORIZONTAL_ALIGN_JUSTIFIED, "Justified"),
    ]
    
    board = models.ForeignKey("VestaBoard", on_delete=models.CASCADE)
    message = models.TextField()
    transition = models.CharField(choices=ANIMATION_CHOICES)
    vertical_alignment = models.CharField(choices=VERTICAL_ALIGN_CHOICES, null=True, default=None)
    horizontal_alignment = models.CharField(choices=HORIZONTAL_ALIGN_CHOICES, null=True, default=None)
    
    def send(self):
        vb = PyVestaBoard(self.board.ip, self.board.port, self.board.api_token)
        vb.send_message(self.message, self.vertical_alignment, self.horizontal_alignment)


class VestaBoard(models.Model):
        ip = models.GenericIPAddressField()
        port = models.IntegerField()
        api_token = models.CharField()
        
        def get_headers(self):
            headers = {
                "X-Vestaboard-Local-Api-Key": f"{self.api_token}"
            }
            return headers
        
        def get_raw_message(self) -> list[list[str]]:
            print(f"{self.ip}:{self.port} - {self.api_token}")
            vb = PyVestaBoard(self.ip, self.port, self.api_token)
            return vb.get_raw_message()
        
        def get_encoded_message(self) -> list[list[str]]:
            # FIXME: Add tests and custom exceptions
            try:
                raw_message = self.get_raw_message()
            except CommunicationException as ex:
                raw_message = PyVestaBoard.format_message(
                    str(ex), PyVestaBoard.VERTICAL_ALIGN_TOP, PyVestaBoard.HORIZONTAL_ALIGN_CENTER
                )
            decoded_message = PyVestaBoard.blank_message()
            for i, row in enumerate(raw_message):
                for j, code in enumerate(row):
                    decoded_message[i][j] = VestaCodes.from_code(code)
            return decoded_message
        
        @classmethod
        def get_str_encoded_message(cls, raw_message) -> list[list[str]]:
            decoded_message = PyVestaBoard.blank_message()
            for i, row in enumerate(raw_message):
                for j, code in enumerate(row):
                    decoded_message[i][j] = VestaCodes.from_code(code)
            return decoded_message
        
        def get_current_message(self) -> str:
            print(f"{self.ip}:{self.port} - {self.api_token}")
            vb = PyVestaBoard(self.ip, self.port, self.api_token)
            return vb.get_current_message()
        
        def send_message(
            self,
            message: str,
            vertical_alignment: str = PyVestaBoard.VERTICAL_ALIGN_MIDDLE,
            horizontal_alignment: str = PyVestaBoard.HORIZONTAL_ALIGN_CENTER,
        ) -> None:
            vm = VestaMessage()
            vm.board = self
            vm.message = message
            vm.vertical_alignment = vertical_alignment
            vm.horizontal_alignment = horizontal_alignment
            vm.save()
            vm.send()
        
        def __str__(self):
            return f"VestaBoard ({self.id}) - {self.ip}"
