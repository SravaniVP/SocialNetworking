# forms.py
from django import forms
from .models import *

class StatusForm(forms.ModelForm):

	class Meta:
		model = Status
		fields = ['description', 'status_Img']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content',]
