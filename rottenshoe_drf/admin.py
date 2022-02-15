from django.contrib import admin
from .models import SneakerFeatures

# Register your models here.

class SneakerReaturesAdmin(admin.ModelAdmin):
    list_display = ('sneaker_name', 'comfortable','grip','spotlight','convenience')

    @admin.display(description="모델이름")
    def sneaker_name(self,data):
        return data.sneaker.sneaker_name


admin.site.register(SneakerFeatures,SneakerReaturesAdmin)