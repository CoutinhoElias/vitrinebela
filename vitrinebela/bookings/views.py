from datetime import date

from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from vitrinebela.bookings.forms import BookingsForm
from vitrinebela.bookings.models import Booking
from vitrinebela.bookings.serializer import BookingSerializer


def scheduling(request):
    context = {
        'form': BookingsForm(initial={'user': request.user})
    }
    return render(request, 'bookings/scheduling_form.html', context)

class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


def list(request):
    selected_date = date.today()
    return list_date(request) #return list_date(request, selected_date.year, selected_date.month)


def list_date(request):
    return render(request, 'bookings/bookings_list.html') #def list_date(request, year, month):


# def _calendar(selected_date):
#     year, month = selected_date.year, selected_date.month
#     filters = {'start__year':  year, 'start__month': month}
#     bookings = {b.start: b for b in Booking.objects.filter(**filters)}
#     calendar = Calendar(firstweekday=6)
#     for week in calendar.monthdatescalendar(year, month):
#         yield [(day, bookings.get(day)) for day in week]
