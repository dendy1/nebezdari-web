from .models import Post, Category
from django import forms
from django_select2.forms import Select2MultipleWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class PostForm(forms.ModelForm):

    title = forms.CharField(
        max_length=256,
        label="Название статьи",
        widget=forms.TextInput(
            attrs={'class': 'input-1'}
        )
    )

    text = forms.CharField(
        widget=CKEditorUploadingWidget(
            attrs={}
        )
    )

    categories = forms.ModelMultipleChoiceField(
        label='Категории',
        queryset=Category.objects.all(),
        widget=Select2MultipleWidget(
            attrs={'class': 'input-1'}
        )
    )

    class Meta:
        model = Post
        fields = ('title', 'text', 'categories')