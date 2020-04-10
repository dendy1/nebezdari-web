from django import forms
from tinymce.widgets import TinyMCE

class PostForm(forms.Form):
    title = forms.CharField(max_length=256)
    cut = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    text = forms.CharField(widget=TinyMCE())