from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from .models import Post, Category

class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=256,
                            label="Название статьи",
                            widget=forms.TextInput(attrs={'class':'input-1'}))
    text = forms.CharField(widget=CKEditorUploadingWidget())
    categories = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Category.objects.all()
    )

    class Meta:
        model = Post
        fields = ('title', 'text', 'categories')