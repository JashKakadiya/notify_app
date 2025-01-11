from django.contrib import admin
from .models import Request_approve, User_Table
from django.utils.html import format_html



admin.site.register(Request_approve)
admin.site.register(User_Table)
