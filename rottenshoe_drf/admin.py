from django.contrib import admin

# Register your models here.

class SneakerReaturesAdmin(admin.ModelAdmin):
    list_display = ('sneaker', 'comfortable','grip','spotligth','convenience')