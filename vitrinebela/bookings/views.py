from datetime import date

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from vitrinebela.bookings.forms import BookingsForm
from vitrinebela.bookings.models import Booking
from vitrinebela.bookings.serializer import BookingSerializer


def scheduling2(request):
    if request.method == 'POST':
        form = BookingsForm(request.POST, request.FILES)

        if not form.is_valid():
            return render(request, 'bookings/scheduling_form.html', {'form':form})

        user = form.cleaned_data.get('user')
        allday = form.cleaned_data.get('allday')
        title = form.cleaned_data.get('title')
        start = form.cleaned_data.get('start')
        end = form.cleaned_data.get('end')
        authorized = form.cleaned_data.get('authorized')
        created_on = form.cleaned_data.get('created_on')
        editable = form.cleaned_data.get('editable')
        color = form.cleaned_data.get('color')
        backgroundColor = form.cleaned_data.get('backgroundColor')
        feriado = form.cleaned_data.get('feriado')
        participants = form.cleaned_data.get('participants')

        Booking.objects.create(user=user,
                               allday=allday,
                               title=title,
                               start=start,
                               end=end,
                               authorized=authorized,
                               created_on=created_on,
                               editable=editable,
                               color=color,
                               backgroundColor=backgroundColor,
                               feriado=feriado,
                               participants=participants)
        form.save_m2m()


        return HttpResponseRedirect('/reserva/listagem/')
    else:
        return render(request, 'bookings/scheduling_form.html', {'form':BookingsForm(initial={'pessoa': request.user.id})})


def scheduling(request):
    if request.method == 'POST':
        form = BookingsForm(request.POST)

        if form.is_valid():
<<<<<<< HEAD
            new = form.save(commit=False)
            new.save()
            form.save_m2m()

=======
            form.save()
            form.save_m2m()
>>>>>>> ea5135590280145224b17f9e3d1dc2a4d2847fd9
            return HttpResponseRedirect('/reserva/listagem/')
        else:
            return render(request, 'bookings/scheduling_form.html', {'form':form})
    else:
        context = {'form':BookingsForm(initial={'pessoa': request.user.id})}
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
