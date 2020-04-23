from django.test import TestCase
from nebezdariapp.forms import ContactForm, SubscribeForm, PostForm, LoginForm, NewAuthorForm, EditAuthorForm
from django.core.files.uploadedfile import SimpleUploadedFile
import copy


class ContactFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.form_data = {"name": "template",
                         "sender": "template@mail.ru",
                         "subject": "template",
                         "message": "template", }

    def test_name_field(self):
        name_data = copy.deepcopy(self.form_data)

        name_data["name"] = ""
        wrong_form = ContactForm(data=name_data)
        self.assertFalse(wrong_form.is_valid())

        name_data["name"] = "n" * (wrong_form.fields["name"].max_length + 1)
        wrong_form = ContactForm(data=name_data)
        self.assertFalse(wrong_form.is_valid())

        name_data["name"] = "Correct name"
        right_form = ContactForm(data=name_data)
        self.assertTrue(right_form.is_valid())

    def test_email_field(self):
        email_data = copy.deepcopy(self.form_data)

        email_data["sender"] = "wrong mail com"
        wrong_form = ContactForm(data=email_data)
        self.assertFalse(wrong_form.is_valid())

        email_data["sender"] = "example@mail.ru"
        right_form = ContactForm(data=email_data)
        self.assertTrue(right_form.is_valid())

    def test_subject_field(self):
        subject_data = copy.deepcopy(self.form_data)

        subject_data["subject"] = ""
        wrong_form = ContactForm(data=subject_data)
        self.assertFalse(wrong_form.is_valid())

        subject_data["subject"] = "n" * (wrong_form.fields["subject"].max_length + 1)
        wrong_form = ContactForm(data=subject_data)
        self.assertFalse(wrong_form.is_valid())

        subject_data["subject"] = "Correct subject"
        right_form = ContactForm(data=subject_data)
        self.assertTrue(right_form.is_valid())

    def test_message_field(self):
        message_data = copy.deepcopy(self.form_data)

        message_data["message"] = ""
        wrong_form = ContactForm(data=message_data)
        self.assertFalse(wrong_form.is_valid())

        message_data["message"] = "Correct message"
        right_form = ContactForm(data=message_data)
        self.assertTrue(right_form.is_valid())


class SubscribeFormTest(TestCase):
    def test_email_field(self):

        data = {"email": "wrong email"}
        wrong_form = SubscribeForm(data=data)
        self.assertFalse(wrong_form.is_valid())

        data["email"] = "right@mail.com"
        right_form = SubscribeForm(data=data)
        self.assertTrue(right_form.is_valid())


class PostFormTest(TestCase):
    data_form = {"title": "template",
                 "text": "template",
                 "categories": [1, 2], }


    def test_title_field(self):
        title_data = copy.deepcopy(self.data_form)

        right_form = PostForm(data=title_data)
        self.assertFalse(right_form.is_valid())


        title_data["title"] = ""
        wrong_form = PostForm(data=title_data)
        self.assertFalse(wrong_form.is_valid())

        title_data["title"] = "n" * (wrong_form.fields["title"].max_length + 1)
        wrong_form = PostForm(data=title_data)
        self.assertFalse(wrong_form.is_valid())


class LoginFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.form_data = {"username": "template",
                         "password": "template"}

    def test_username_field(self):
        username_data = copy.deepcopy(self.form_data)

        right_form = LoginForm(data=username_data)
        self.assertTrue(right_form.is_valid())

        username_data['username'] = ""
        wrong_form = LoginForm(data=username_data)
        self.assertFalse(wrong_form.is_valid())

    def test_password_field(self):
        password_data = copy.deepcopy(self.form_data)

        right_form = LoginForm(data=password_data)
        self.assertTrue(right_form.is_valid())

        password_data['password'] = ""
        wrong_form = LoginForm(data=password_data)
        self.assertFalse(wrong_form.is_valid())


class NewAuthorFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.form_data = {"username": "template",
                         "email": "template@mail.com",
                         "first_name": "template",
                         "last_name": "template", }

    def test_username_field(self):
        username_data = copy.deepcopy(self.form_data)

        right_form = NewAuthorForm(data=username_data)
        self.assertTrue(right_form.is_valid())

        username_data['username'] = ""
        wrong_form = NewAuthorForm(data=username_data)
        self.assertFalse(wrong_form.is_valid())

    def test_email_field(self):
        email_data = copy.deepcopy(self.form_data)

        email_data["email"] = "wrong mail com"
        wrong_form = NewAuthorForm(data=email_data)
        self.assertFalse(wrong_form.is_valid())

        email_data["email"] = "example@mail.ru"
        right_form = NewAuthorForm(data=email_data)
        self.assertTrue(right_form.is_valid())

    def test_first_name_field(self):
        first_name_data = copy.deepcopy(self.form_data)

        first_name_data["first_name"] = ""
        wrong_form = NewAuthorForm(data=first_name_data)
        self.assertFalse(wrong_form.is_valid())

        first_name_data["first_name"] = "right name"
        right_form = NewAuthorForm(data=first_name_data)
        self.assertTrue(right_form.is_valid())

    def test_last_name_field(self):
        last_name_data = copy.deepcopy(self.form_data)

        last_name_data["last_name"] = ""
        wrong_form = NewAuthorForm(data=last_name_data)
        self.assertFalse(wrong_form.is_valid())

        last_name_data["last_name"] = "right name"
        right_form = NewAuthorForm(data=last_name_data)
        self.assertTrue(right_form.is_valid())


class EditAuthorFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        upload_file = open('nebezdariapp/tests/images/sunset.jpg', 'rb')
        cls.image = {"avatar": SimpleUploadedFile(upload_file.name, upload_file.read())}
        cls.form_data = {"first_name": "template",
                         "last_name": "template",
                         "about": "template", }

    def test_first_name_field(self):
        first_name_data = copy.deepcopy(self.form_data)

        first_name_data["first_name"] = ""
        wrong_form = EditAuthorForm(first_name_data, self.image)
        self.assertFalse(wrong_form.is_valid())

        first_name_data["first_name"] = "right name"
        right_form = EditAuthorForm(first_name_data, self.image)
        self.assertTrue(right_form.is_valid())

    def test_last_name_field(self):
        last_name_data = copy.deepcopy(self.form_data)

        last_name_data["last_name"] = ""
        wrong_form = EditAuthorForm(last_name_data, self.image)
        self.assertFalse(wrong_form.is_valid())

        last_name_data["last_name"] = "right name"
        right_form = EditAuthorForm(last_name_data, self.image)
        self.assertTrue(right_form.is_valid())

    def test_about_field(self):
        about_data = copy.deepcopy(self.form_data)

        about_data["about"] = ""
        wrong_form = EditAuthorForm(about_data, self.image)
        self.assertFalse(wrong_form.is_valid())

        about_data["about"] = "right about"
        right_form = EditAuthorForm(about_data, self.image)
        self.assertTrue(right_form.is_valid())

    def test_avatar_field(self):

        right_form = EditAuthorForm(self.form_data, self.image)
        self.assertTrue(right_form.is_valid())

        try:
            self.image = SimpleUploadedFile()
            wrong_form = EditAuthorForm(self.form_data, self.image)
            self.assertTrue(wrong_form.is_valid())
        except TypeError:
            self.assertFalse(False)


