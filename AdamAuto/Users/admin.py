from django.contrib import admin
from .models import User

class UsersAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'username', 'password')
    search_fields = ('name', 'email', 'username')

admin.site.register(User)
