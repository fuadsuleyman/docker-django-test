from django.contrib import admin

# Register your models here.

from .models import Customer

# admin.site.register(Customer)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "device")
    list_display_links = ("device",)