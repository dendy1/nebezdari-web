from django.contrib import admin

from .models import Authors, Categories, Comments, Posts, MailingMembers

admin.site.register(Authors)
admin.site.register(Categories)
admin.site.register(Comments)
admin.site.register(Posts)
admin.site.register(MailingMembers)
