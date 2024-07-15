from django import forms
from .models import RoomMessage

class RoomMessageForm(forms.ModelForm):
    
    class Meta:
        model = RoomMessage
        fields = ("body",)

