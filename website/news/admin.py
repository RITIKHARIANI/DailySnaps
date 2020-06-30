from django.contrib import admin
from .models import News,Profile,Saved_Articles

admin.site.register(News)
admin.site.register(Profile)
admin.site.register(Saved_Articles)