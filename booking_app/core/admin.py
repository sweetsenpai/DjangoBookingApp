from django.contrib import admin

from .models import Booking, Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price_per_day", "capacity")
    list_filter = ("price_per_day", "capacity")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "room", "user", "date_start", "date_end")
    list_filter = ("room", "user", "date_start")
    search_fields = ("room__name", "user__username")
