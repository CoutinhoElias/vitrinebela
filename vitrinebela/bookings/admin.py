from django.contrib import admin
from vitrinebela.bookings.models import Booking


class BookingModelAdmin(admin.ModelAdmin):
    pass

admin.site.register(Booking, BookingModelAdmin)
