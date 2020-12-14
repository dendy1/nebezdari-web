from snowpenguin.django.recaptcha3.fields import ReCaptchaField

from .models import Post, Category, Author, Comment
from django import forms
from django_select2.forms import Select2MultipleWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostForm(forms.ModelForm):
    """
    Форма для создания/редактирования информации о посте
    """

    # Текстовое поле для Заголовка статьи
    title = forms.CharField(
        max_length=256,
        label="Название статьи",
        widget=forms.TextInput(
            attrs={'class': 'input-1'}
        )
    )

    # Текстовое поле для Текста статьи
    text = forms.CharField(
        label='Текст статьи',
        widget=CKEditorUploadingWidget
    )

    # Выпадающий список для выбора Категорий для статьи
    categories = forms.ModelMultipleChoiceField(
        label='Категории',
        queryset=Category.objects.all(),
        widget=Select2MultipleWidget(
            attrs={'class': 'input-1'}
        )
    )

    # Поле для выбора картинки-превью
    image = forms.ImageField(
         label='Картинка-превью',
         required=False
    )

    class Meta:
        model = Post
        fields = ('title', 'text', 'categories', 'image')

class NewAuthorForm(forms.ModelForm):
    """
    Форма для добавления (регистрации) нового автора
    """

    # Текстовое поле для Логина автора
    username = forms.CharField(
        label='Логин нового автора',
        widget=forms.TextInput(
            attrs={'class': 'input-1', 'placeholder': 'Введите логин'}
        ),
        required=True
    )

    # Текстовое поле для E-Mail автора
    email = forms.CharField(
        label='E-mail нового автора',
        widget=forms.EmailInput(
            attrs={'class': 'input-1', 'placeholder': 'Введите E-Mail'}
        ),
        required=True
    )

    # Текстовое поле для Имя автора
    first_name = forms.CharField(
        label='Имя нового автора',
        widget=forms.TextInput(
            attrs={'class': 'input-1', 'placeholder': 'Введите имя'}
        ),
        required=False
    )

    # Текстовое поле для Фамилии автора
    last_name = forms.CharField(
        label='Фамилия нового автора',
        widget=forms.TextInput(
            attrs={'class': 'input-1', 'placeholder': 'Введите фамилию'}
        ),
        required=False
    )

    class Meta:
        model = Author
        fields = ('username', 'email', 'first_name', 'last_name')

class EditAuthorForm(forms.ModelForm):
    """
    Форма для редактирования информации об авторе
    """

    # Текстовое поле для Имя автора
    first_name = forms.CharField(
        label='Имя нового автора',
        widget=forms.TextInput(
            attrs={'class': 'input-1', 'placeholder': 'Введите имя'}
        )
    )

    # Текстовое поле для Фамилии автора
    last_name = forms.CharField(
        label='Фамилия нового автора',
        widget=forms.TextInput(
            attrs={'class': 'input-1', 'placeholder': 'Введите фамилию'}
        )
    )

    # Текстовое поле для Личной информации об авторе
    about = forms.CharField(
        label='Краткая информация',
        widget=CKEditorUploadingWidget,
        required=False
    )

    # Поле для выбора картинки-аватара
    avatar = forms.ImageField()

    class Meta:
        model = Author
        fields = ('first_name', 'last_name', 'about', 'avatar')

class LoginForm(forms.Form):
    """
    Форма для авторизации
    """

    # Текстовое поле для логина
    username = forms.CharField(
        label='Логин или E-Mail',
        widget=forms.TextInput(
            attrs={'class': 'input-1', 'placeholder': 'Введите логин или E-Mail'}
        )
    )

    # Текстовое поле для пароля
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={'class': 'input-1', 'placeholder': 'Введите пароль'}
        )
    )


class ContactForm(forms.Form):
    """
    Форма обратной связи для отправки сообщения по E-Mail
    """

    # Поле для каптчи
    captcha = ReCaptchaField()

    # Текстовое поле для Имя отправителя
    name = forms.CharField(
        label="Имя",
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'input-1', 'placeholder': 'Введите имя'}
        )
    )

    # Текстовое поле для E-Mail обратной связи
    sender = forms.EmailField(
        label="E-mail",
        widget=forms.TextInput(
            attrs={'class': 'input-1', 'placeholder': 'Введите e-mail'}
        )
    )

    # Текстовое поле для Темы сообщения
    subject = forms.CharField(
        label="Тема",
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'input-1', 'placeholder': 'Введите тему сообщения'}
        )
    )

    # Текстовое поле для Текста сообщения
    message = forms.CharField(
        label="Сообщение",
        widget=forms.Textarea(
            attrs={'placeholder': 'Введите сообщение'}
        )
    )


class SubscribeForm(forms.Form):
    """
    Форма для подписки на обновления сайта
    """

    # Текстовое поле для E-Mail подписчика
    email = forms.EmailField()

class CategoriesForm(forms.Form):
    """
    Форма для выбора категорий для фильтрации постов
    """

    # Выпадающий список для выбора Категорий для статьи
    categories = forms.ModelMultipleChoiceField(
        label='Категории',
        queryset=Category.objects.all(),
        widget=Select2MultipleWidget(
            attrs={'class': 'input-1'}
        ),
        required=False,
        help_text='Выберите категории'
    )

class CommentForm(forms.ModelForm):
    """
    Форма для отправки сообщения под постом
    """

    # Поле для каптчи
    captcha = ReCaptchaField()

    # Текстовое поле для Имя автора сообщения
    name = forms.CharField(
        max_length=64,
        label="Имя",
        widget=forms.TextInput(
            attrs={
                'class':'bg-cinput'
            }
        )
    )

    # Текстовое поле для Текста сообщения
    text = forms.CharField(
        max_length=512,
        label="Текст сообщения",
        widget=forms.Textarea(
            attrs={
                'class':'bg-ctexteria',
                'style':'resize: vertical'
            }
        )
    )

    # Скрытое числовое поле, содержащее ID родительского комментария
    parent_comment = forms.IntegerField(
        widget=forms.HiddenInput,
        required=False
    )

    class Meta:
        model = Comment
        fields = ('name', 'text')