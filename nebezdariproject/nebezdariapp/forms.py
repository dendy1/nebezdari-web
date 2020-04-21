from .models import Post, Category, Author, Comment
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


class ContactForm(forms.Form):
    name = forms.CharField(
        label="Имя",
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'input-1', 'placeholder': 'Введите имя'}
        )
    )
    sender = forms.EmailField(
        label="E-mail",
        widget=forms.TextInput(
            attrs={'class': 'input-1', 'placeholder': 'Введите e-mail'}
        )
    )
    subject = forms.CharField(
        label="Тема",
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'input-1', 'placeholder': 'Введите тему сообщения'}
        )
    )
    message = forms.CharField(
        label="Сообщение",
        widget=forms.Textarea(
            attrs={'placeholder': 'Введите сообщение'}
        )
    )


class SubscribeForm(forms.Form):
    email = forms.EmailField()

class CommentForm(forms.ModelForm):
    name = forms.CharField(
        max_length=64,
        label="Имя",
        widget=forms.TextInput(
            attrs={
                'class':'bg-cinput'
            }
        )
    )

    text = forms.CharField(
        max_length=64,
        label="Текст сообщения",
        widget=forms.Textarea(
            attrs={
                'class':'bg-ctexteria',
                'style':'resize: vertical'
            }
        )
    )

    parent_comment = forms.IntegerField(
        widget=forms.HiddenInput,
        required=False
    )

    class Meta:
        model = Comment
        fields = ('name', 'text')