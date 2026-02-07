import requests
import math
import json
import regex

from django.db import models

CODES = {
	" ": {
		"name": "Blank",
		"code": 0
	},
	"A": {
		"name":	"A",
		"code": 1
	},
	"B": {
		"name":	"B",
		"code": 2
	},
	"C": {
		"name":	"C",
		"code": 3
	},
	"D": {
		"name":	"D",
		"code": 4
	},
	"E": {
		"name":	"E",
		"code": 5
	},
	"F": {
		"name":	"F",
		"code": 6
	},
	"G": {
		"name":	"G",
		"code": 7
	},
	"H": {
		"name":	"H",
		"code": 8
	},
	"I": {
		"name":	"I",
		"code": 9
	},
	"J": {
		"name":	"J",
		"code": 10
	},
	"K": {
		"name":	"K",
		"code": 11
	},
	"L": {
		"name":	"L",
		"code": 12
	},
	"M": {
		"name":	"M",
		"code": 13
	},
	"N": {
		"name":	"N",
		"code": 14
	},
	"O": {
		"name":	"O",
		"code": 15
	},
	"P": {
		"name":	"P",
		"code": 16
	},
	"Q": {
		"name":	"Q",
		"code": 17
	},
	"R": {
		"name":	"R",
		"code": 18
	},
	"S": {
		"name":	"S",
		"code": 19
	},
	"T": {
		"name":	"T",
		"code": 20
	},
	"U": {
		"name":	"U",
		"code": 21
	},
	"V": {
		"name":	"V",
		"code": 22
	},
	"W": {
		"name":	"W",
		"code": 23
	},
	"X": {
		"name":	"X",
		"code": 24
	},
	"Y": {
		"name":	"Y",
		"code": 25
	},
	"Z": {
		"name":	"Z",
		"code": 26
	},
	"1": {
		"name":	"One",
		"code": 27
	},
	"2": {
		"name":	"Two",
		"code": 28
	},
	"3": {
		"name":	"Three",
		"code": 29
	},
	"4": {
		"name":	"Four",
		"code": 30
	},
	"5": {
		"name":	"Five",
		"code": 31
	},
	"6": {
		"name":	"Six",
		"code": 32
	},
	"7": {
		"name":	"Seven",
		"code": 33
	},
	"8": {
		"name":	"Eight",
		"code": 34
	},
	"9": {
		"name":	"Nine",
		"code": 35
	},
	"0": {
		"name":	"Zero",
		"code": 36
	},
	"!": {
		"name": "Exclamation Mark",
		"code": 37
	},
	"@": {
		"name": "At",
		"code": 38
	},
	"#": {
		"name": "Pound",
		"code": 39
	},
	"$": {
		"name": "Dollar",
		"code": 40
	},
	"(": {
		"name": "Left Parenthesis",
		"code": 41
	},
	")": {
		"name": "Right Parenthesis",
		"code": 42
	},
	"-": {
		"name": "Hyphen",
		"code": 44
	},
	"+": {
		"name": "Plus",
		"code": 46
	},
	"&": {
		"name": "Ampersand",
		"code": 47
	},
	"=": {
		"name": "Equal",
		"code": 48
	},
	";": {
		"name": "Semicolon",
		"code": 49
	},
	":": {
		"name": "Colon",
		"code": 50
	},
	"'": {
		"name": "Single Quote",
		"code": 52
	},
	'"': {
		"name": "Double Quote",
		"code": 53
	},
	"%": {
		"name": "Percent",
		"code": 54
	},
	",": {
		"name": "Comma",
		"code": 55
	},
	".": {
		"name": "Period",
		"code": 56
	},
	"/": {
		"name": "Slash",
		"code": 59
	},
	"?": {
		"name": "Question Mark",
		"code": 60
	},
	"°": {
		"name": "Degree",
		"code": 62
	},
	"🟥": {
		"name": "PoppyRed",
		"code": 63
	},
	"🟧": {
		"name": "Orange",
		"code": 64
	},
	"🟨": {
		"name": "Yellow",
		"code": 65
	},
	"🟩": {
		"name": "Green",
		"code": 66
	},
	"🟦": {
		"name": "ParisBlue",
		"code": 67
	},
	"🟪": {
		"name": "Violet",
		"code": 68
	},
	"⬜️": {
		"name": "White",
		"code": 69
	},
	"⬜": {
		"name": "White",
		"code": 69
	},
}

COLUMNS = 22
ROWS = 6


class VestaCodes:
	def valid(self, character: str) -> bool:
		return character in CODES.keys()

	def to(self, character: str) -> int:
		try:
			return CODES[character].get("code")
		except KeyError:
			print(f"Ignoring code: '{character}'")
			return -1
	
	def from_code(self, code: int) -> str:
		for key, character in CODES.items():
			if character['code'] == code:
				return key


class VestaMessage(models.Model):
	ANIMATION_COLUMN = "column"  # "Wave" in the app.
	ANIMATION_REVERSE_COLUMN = "reverse-column"  # "Drift" in the app.
	ANIMATION_EDGES_TO_CENTER = "edges-to-center"  # "Curtain" in the app.
	ANIMATION_ROW = "row" # Row-by-row animation. Not available in the app.
	ANIMATION_DIAGONAL = "diagonal"  # Corner-to-corner animation. Not available in the app.
	ANIMATION_RANDOM = "random"  # Animates the number in step_size at a time randomly.
	ANIMATION_CHOICES = [
		(ANIMATION_COLUMN, "Column"),
		(ANIMATION_REVERSE_COLUMN, "Reverse Column"),
		(ANIMATION_EDGES_TO_CENTER, "Edges to Center"),
		(ANIMATION_ROW, "Row"),
		(ANIMATION_DIAGONAL, "Diagonal"),
		(ANIMATION_RANDOM, "Random"),
	]
	
	VERTICAL_ALIGN_TOP = "top"
	VERTICAL_ALIGN_MIDDLE = "middle"
	VERTICAL_ALIGN_BOTTOM = "bottom"
	VERTICAL_ALIGN_JUSTIFIED = "justified"
	VERTICAL_ALIGN_CHOICES = [
		(VERTICAL_ALIGN_TOP, "Top"),
		(VERTICAL_ALIGN_MIDDLE, "Middle"),
		(VERTICAL_ALIGN_BOTTOM, "Bottom"),
		(VERTICAL_ALIGN_JUSTIFIED, "Justified"),
	]
	
	HORIZONTAL_ALIGN_LEFT = "top"
	HORIZONTAL_ALIGN_CENTER = "middle"
	HORIZONTAL_ALIGN_RIGHT = "bottom"
	HORIZONTAL_ALIGN_JUSTIFIED = "justified"
	HORIZONTAL_ALIGN_CHOICES = [
		(HORIZONTAL_ALIGN_LEFT, "Left"),
		(HORIZONTAL_ALIGN_CENTER, "Center"),
		(HORIZONTAL_ALIGN_RIGHT, "Right"),
		(HORIZONTAL_ALIGN_JUSTIFIED, "Justified"),
	]
	
	board = models.ForeignKey("VestaBoard", on_delete=models.CASCADE)
	message = models.TextField()
	transition = models.CharField(choices=ANIMATION_CHOICES)
	vertical_alignment = models.CharField(choices=VERTICAL_ALIGN_CHOICES, null=True, default=None)
	horizontal_alignment = models.CharField(choices=HORIZONTAL_ALIGN_CHOICES, null=True, default=None)
	
	@classmethod
	def blank_message(cls):
		encoded_message = [[], [], [], [], [], []]
		for idx in range(0, 6):
			encoded_message += []
			for j in range(0, 22):
				encoded_message[idx] += [0]
		return encoded_message
	
	@classmethod
	def format_message(cls, message: str, vertical_alignment: str, horizontal_alignment: str):
		message_chars = regex.findall(r"\X", message)
		message_rows = []
		index = 0
		cur_row = []
		for char in message_chars:
			if char == "\n":
				index = 0
				if len(cur_row) > 0:
					message_rows += [cur_row]
				cur_row = []
				continue
			cur_row += [char]
			if index == 21:
				index = 0
				message_rows += [cur_row]
				cur_row = []
			index += 1
		if len(cur_row) > 0:
			message_rows += [cur_row]
		
		if len(message_rows) > 6:
			raise Exception("Message has too many rows")
		
		t_padding = 0
		match vertical_alignment:
			case cls.VERTICAL_ALIGN_TOP:
				t_padding = 0
			case cls.VERTICAL_ALIGN_MIDDLE:
				t_padding = int((ROWS - len(message_rows)) / 2)
			case cls.VERTICAL_ALIGN_BOTTOM:
				t_padding = int(ROWS - len(message_rows))
		
		c = VestaCodes()
		encoded_message = cls.blank_message()
		for row, row_message_chars in enumerate(message_rows):
			l_padding = 0
			match horizontal_alignment:
				case cls.HORIZONTAL_ALIGN_LEFT:
					pass
				case cls.HORIZONTAL_ALIGN_CENTER:
					if len(row_message_chars) < COLUMNS:
						l_padding = int((COLUMNS - len(row_message_chars))/2)
				case cls.HORIZONTAL_ALIGN_RIGHT:
					if len(row_message_chars) < COLUMNS:
						l_padding = int((COLUMNS - len(row_message_chars)))
		
			for i, char in enumerate(row_message_chars):
				encoded_message[row + t_padding][l_padding + i] = c.to(char.upper())
		return encoded_message
	
	def send(self):
		encoded_message = VestaMessage.format_message(self.message, self.vertical_alignment, self.horizontal_alignment)
		
		post_data = {
			"characters": encoded_message,
			"ANIMATION": "random",
			"step_size": 22*6,
		}
		r = requests.post(
			f"http://{self.board.ip}:{self.board.port}/local-api/message",
			headers=self.board.get_headers(),
			data=json.dumps(post_data)
		)


class VestaBoard(models.Model):
		ip = models.GenericIPAddressField()
		port = models.IntegerField()
		api_token = models.CharField()
		
		def get_headers(self):
			headers = {
				"X-Vestaboard-Local-Api-Key": f"{self.api_token}"
			}
			return headers
		
		def get_message(self):
			response = requests.get(f"http://{self.ip}:{self.port}/local-api/message", headers=self.get_headers())
			if response.ok:
				data = response.json()
				vm = VestaMessage()
				vc = VestaCodes()
				decoded_message = vm.blank_message()
				for i, row in enumerate(data['message']):
					for j, code in enumerate(row):
						decoded_message[i][j] = vc.from_code(code)
				return decoded_message
		
		def send_message(
			self,
			message: str,
			vertical_alignment: str = VestaMessage.VERTICAL_ALIGN_MIDDLE,
			horizontal_alignment: str = VestaMessage.HORIZONTAL_ALIGN_CENTER,
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
