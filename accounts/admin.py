from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
from django.utils.html import format_html
# Register your models here.
class AccountAdmin(UserAdmin):
    list_display=('email','username','first_name','last_name','is_active','last_logined')
    list_display_links=('email','username')
    ordering=('-date_joined',)
    filter_horizontal=()
    list_filter=()
    fieldsets=()
    
admin.site.register(models.Account,AccountAdmin)
    
    
class userprofileadmin(admin.ModelAdmin):
    def thumbnail(self,object):
        return format_html('<img src="{}" width="30" height="30" style="border-border-radius:50%">'.format(object.profile_picture.url))
    thumbnail.short_description='Profile Picture'
    list_display=('thumbnail','user','city','state','country',)

admin.site.register(models.UserProfile,userprofileadmin)