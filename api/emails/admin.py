from django.contrib import admin
from .models import User, Email, ScanResult

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'role', 'is_active', 'created_at')
    search_fields = ('email', 'name')

@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sender', 'recipient', 'received_at', 'processed')
    search_fields = ('subject', 'body')

@admin.register(ScanResult)
class ScanResultAdmin(admin.ModelAdmin):
    list_display = ('email', 'result', 'confidence', 'scanned_at')
    search_fields = ('result',)
