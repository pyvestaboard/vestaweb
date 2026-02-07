from django.contrib import admin

from .models import VestaBoard, VestaMessage

@admin.register(VestaMessage)
class VestaMessageAdmin(admin.ModelAdmin):
	list_display = ["board", "message", "transition", "vertical_alignment", "horizontal_alignment"]

admin.site.register(VestaBoard)
