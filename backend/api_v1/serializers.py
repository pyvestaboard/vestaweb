from rest_framework import serializers

from pyvestaboard import VestaBoard as PyVestaBoard


class RelayMessageSerializer(serializers.Serializer):
	message = serializers.CharField()
	vertical_alignment = serializers.CharField()
	horizontal_alignment = serializers.CharField()
	
	def validate_vertical_alignment(self, value):
		if value not in PyVestaBoard.VERTICAL_ALIGN_OPTIONS:
			raise serializers.ValidationError(f"Vertical alignment needs to be one of {PyVestaBoard.VERTICAL_ALIGN_OPTIONS}")
		return value
	
	def validate_horizontal_alignment(self, value):
		if value not in PyVestaBoard.HORIZONTAL_ALIGN_OPTIONS:
			raise serializers.ValidationError(f"Horizontal alignment needs to be one of {PyVestaBoard.HORIZONTAL_ALIGN_OPTIONS}")
		return value