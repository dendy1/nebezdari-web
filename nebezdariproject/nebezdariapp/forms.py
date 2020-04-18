from .models import Post, Category, Author
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
        label='Текст статьи',
        widget=CKEditorUploadingWidget
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

class NewAuthorForm(forms.ModelForm):
    username = forms.CharField(
        label='Логин нового автора',
        widget=forms.TextInput(
            attrs={'class': 'input-1', 'placeholder': 'Введите логин'}
        )
    )

    email = forms.CharField(
        label='E-mail нового автора',
        widget=forms.EmailInput(
            attrs={'class': 'input-1', 'placeholder': 'Введите E-Mail'}
        )
    )

    first_name = forms.CharField(
        label='Имя нового автора',
        widget=forms.TextInput(
            attrs={'class': 'input-1', 'placeholder': 'Введите имя'}
        )
    )

    last_name = forms.CharField(
        label='Фамилия нового автора',
        widget=forms.TextInput(
            attrs={'class': 'input-1', 'placeholder': 'Введите фамилию'}
        )
    )

    class Meta:
        model = Author
        fields = ('username', 'email', 'first_name', 'last_name')

class EditAuthorForm(forms.ModelForm):
    first_name = forms.CharField(
        label='Имя нового автора',
        widget=forms.TextInput(
            attrs={'class': 'input-1', 'placeholder': 'Введите имя'}
        )
    )

    last_name = forms.CharField(
        label='Фамилия нового автора',
        widget=forms.TextInput(
            attrs={'class': 'input-1', 'placeholder': 'Введите фамилию'}
        )
    )

    about = forms.CharField(
        label='Краткая информация',
        widget=CKEditorUploadingWidget
    )

    avatar = forms.ImageField()

    class Meta:
        model = Author
        fields = ('first_name', 'last_name', 'about', 'avatar')

class LoginForm(forms.Form):
    username = forms.CharField(
        label='Логин или E-Mail',
        widget=forms.TextInput(
            attrs={'class': 'input-1', 'placeholder': 'Введите логин или E-Mail'}
        )
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={'class': 'input-1', 'placeholder': 'Введите пароль'}
        )
    )