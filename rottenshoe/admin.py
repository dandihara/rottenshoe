from django.contrib import admin

from .models import Sneakers,Keyword,User

# Register your models here.

class SneakerAdmin(admin.ModelAdmin):
    search_fields = ['sneaker_name','model_number']
    list_display = ('sneaker_name','retail_date','brand','price')

class KeywordAdmin(admin.ModelAdmin):
    search_fields = ['keyword']
    list_display = ('keyword','sneaker_id')

class UserAdmin(admin.ModelAdmin):
    search_fields = ['email','nickname']
    list_display = ('email','nickname','created_time','update_time')

admin.site.register(Sneakers,SneakerAdmin)
admin.site.register(Keyword,KeywordAdmin)
admin.site.register(User,UserAdmin)