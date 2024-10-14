from django.contrib import admin

from lists.models import *

# Register your models here.
admin.site.register(AppUser)
admin.site.register(Actor)
admin.site.register(Director)
admin.site.register(Writer)
admin.site.register(Genre)
admin.site.register(Film)
admin.site.register(Sticker)