from django.contrib import admin

from .models import Sneakers,Keyword

# Register your models here.


class BoardAdmin(admin.ModelAdmin):
    search_fields = ['sneaker_name','model_number']

class KeywordAdmin(admin.ModelAdmin):
    search_fields = ['keyword']

admin.site.register(Sneakers,BoardAdmin)
admin.site.register(Keyword,KeywordAdmin)