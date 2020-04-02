from django.db import models

class MailingMembers(models.Model):
    email = models.EmailField(max_length=255)

    def __str__(self):
        print(self.email)

    class Meta:
        db_table = "nebezdariapp_mailing_members"

class Authors(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    login = models.CharField(max_length=64, unique=True)
    password = models.CharField(max_length=64)
    first_name = models.CharField(max_length=64)
    second_name = models.CharField(max_length=64)
    about = models.CharField(max_length=512)

    def __str__(self):
        print(self.login)


class Categories(models.Model):
    name = models.CharField(max_length=63, unique=True)

    def __str__(self):
        print(self.name)


class Posts(models.Model):
    author = models.ForeignKey(Authors, null=True, on_delete=models.SET_NULL)
    text = models.TextField()
    categories = models.ManyToManyField(Categories)
