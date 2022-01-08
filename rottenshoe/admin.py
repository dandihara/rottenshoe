from django.contrib import admin

from .models import Sneakers

# Register your models here.


class BoardAdmin(admin.ModelAdmin):
    search_fields = ['sneaker_name','model_number']


admin.site.register(Sneakers,BoardAdmin)