from django import forms
from tinymce.widgets import TinyMCE

class PostForm(forms.Form):
    CHOICES = (
        "Category 1",
        "Category 2",
        "Category 3",
        "Category 4",
        "Category 5",
        "Category 6",
        "Category 7",
        "Category 8",
    )

    title = forms.CharField(
        label="Заголовок поста",
        max_length=256,
        widget= forms.TextInput(attrs={'class':'input-1'}))
    text = forms.CharField(widget=TinyMCE(attrs={'rows': 40}))
    categories = forms.CheckboxSelectMultiple(choices=CHOICES)