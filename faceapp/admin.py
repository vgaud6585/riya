from django.contrib import admin
from .models import VisitorActivity

# Register your models here.

@admin.register(VisitorActivity)
class VisitorAdmin(admin.ModelAdmin):
	list_display = ('session_key', 'ip_address', 'pages_visited', 'first_seen', 'last_seen', 'duration')