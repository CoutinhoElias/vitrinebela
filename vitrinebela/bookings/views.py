from datetime import date

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from vitrinebela.bookings.forms import BookingsForm
from vitrinebela.bookings.models import Booking
from vitrinebela.bookings.serializer import BookingSerializer


class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


def list(request):
    selected_date = date.today()
    return list_date(request) #return list_date(request, selected_date.year, selected_date.month)


def list_date(request):
    return render(request, 'bookings/bookings_list.html') #def list_date(request, year, month):


def scheduling(request):
    if request.method == 'POST':
        form = BookingsForm(request.POST)

        if form.is_valid():

            new = form.save(commit=False)
            new.save()
            form.save_m2m()

            return HttpResponseRedirect('/reserva/listagem/')
        else:
            return render(request, 'bookings/scheduling_form.html', {'form':form})
    else:
        context = {'form':BookingsForm(initial={'pessoa': request.user.id})}
        return render(request, 'bookings/scheduling_form.html', context)


def scheduling_edit(request, id_booking):
    booking = Booking.objects.get(id=id_booking)
    if request.method == 'GET':
        form = BookingsForm(instance=booking)
    else:
        form = BookingsForm(request.POST, instance=booking)
        if form.is_valid():
            new = form.save(commit=False)
            new.save()
            form.save_m2m()
        return HttpResponseRedirect('/reserva/listagem/')
    return render(request, 'bookings/scheduling_form.html', {'form':form})


# def _calendar(selected_date):
#     year, month = selected_date.year, selected_date.month
#     filters = {'start__year':  year, 'start__month': month}
#     bookings = {b.start: b for b in Booking.objects.filter(**filters)}
#     calendar = Calendar(firstweekday=6)
#     for week in calendar.monthdatescalendar(year, month):
#         yield [(day, bookings.get(day)) for day in week]
