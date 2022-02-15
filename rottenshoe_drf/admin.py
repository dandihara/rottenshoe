from django.contrib import admin
from django.contrib import auth
from models import SneakerFeatures

# Register your models here.

class SneakerReaturesAdmin(admin.ModelAdmin):
    list_display = ('sneaker', 'comfortable','grip','spotligth','convenience')


admin.site.register(SneakerFeatures,SneakerReaturesAdmin)