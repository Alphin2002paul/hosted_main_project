from django.contrib import admin
from .models import Brand, ModelName, CertifiedCar, CertifiedCarImage

class CertifiedCarImageInline(admin.TabularInline):
    model = CertifiedCarImage
    extra = 1

@admin.register(CertifiedCar)
class CertifiedCarAdmin(admin.ModelAdmin):
    list_display = ('manufacturer', 'model_name', 'year', 'price', 'car_status')
    list_filter = ('car_status', 'manufacturer', 'year')
    search_fields = ('manufacturer__company_name', 'model_name__model_name')
    inlines = [CertifiedCarImageInline]

admin.site.register(Brand)
admin.site.register(ModelName)
admin.site.register(CertifiedCarImage) 