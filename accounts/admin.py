from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
# Register your models here.
class AccountAdmin(UserAdmin):
    list_display=('email','username','first_name','last_name','is_active','last_logined')
    list_display_links=('email','username')
    ordering=('-date_joined',)
    filter_horizontal=()
    list_filter=()
    fieldsets=()
admin.site.register(models.Account,AccountAdmin)