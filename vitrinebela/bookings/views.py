from calendar import Calendar
from datetime import date, timedelta, datetime

import simplejson as simplejson
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
from rest_framework.viewsets import ModelViewSet

from vitrinebela.bookings.models import Booking
from vitrinebela.bookings.serializer import BookingSerializer


class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


def home(request):
    return render(request, 'bookings/home.html')


def list(request):
    selected_date = date.today()
    return list_date(request, selected_date.year, selected_date.month)


def list_date(request, year, month):

    try:
        selected_date = date(int(year), int(month), 1)
    except ValueError:
        raise Http404

    context = {
        'selected_date': selected_date,
        'calendar': tuple(_calendar(selected_date)),
        'next': selected_date + timedelta(days=31),
        'previous': selected_date - timedelta(days=1)
    }

    return render(request, 'bookings/bookings_list.html', context)


def _calendar(selected_date):
    year, month = selected_date.year, selected_date.month
    filters = {'start__year':  year, 'start__month': month}
    bookings = {b.start: b for b in Booking.objects.filter(**filters)}
    calendar = Calendar(firstweekday=6)
    for week in calendar.monthdatescalendar(year, month):
        yield [(day, bookings.get(day)) for day in week]

# -------------------------------------------------------------------------------

@csrf_exempt
def creaEventos(request):

    event = {}

    title = request.POST.get("title", "")
    if (title is not None and title != ''):
        event['title'] = title[0:(title.index('-')-1)]
    else:
        event['title'] = ""

    # allDay is received from the POST object as a string - change to boolean
    allDay_str = request.POST.get("allDay", "")
    if(allDay_str == "true"):
        event['allDay'] = True
    else:
        event['allDay'] = False

    start = request.POST.get("start", "")
    start = int(start)/1000

    start = datetime.datetime.fromtimestamp(start).strftime('%Y-%m-%d %H:%M:%S')

    event['start'] = start

    # Set end-date if it exists
    end = request.POST.get("end", "")
    if (end is not None and end != ''):
        end = request.POST.get("end", "")
        end = int(end)/1000
        end = datetime.datetime.fromtimestamp(end).strftime('%Y-%m-%d %H:%M:%S')
        event['end'] = end
    else:
        event['end'] = event['start']

    avaluo_id = request.POST.get("avaluo_id", "")
    if (avaluo_id is not None and avaluo_id != ''):
        event['avaluo_id'] = request.POST.get("avaluo_id", "")

    # Set entry colour if it exists
    color = request.POST.get("color", "")
    if (color is not None and color != ''):
        event['color'] = request.POST.get("color", "")

    # Return the ID of the added (or updated) calendar entry
    output = {}
    # Add or update collection record, determined by whether it has an ID or not
    record_id = request.POST.get("id", "")
    if(record_id is not None and record_id != ''):
        event_id = Booking.objects.filter(booking_id=record_id)
        event_id.update(Inicio=event['start'], Fin=event['end'], diaEntero=event['allDay'], asigna_id=request.user.id)
        output['id'] = record_id
    else:
        avaluo = 'Título inserido na view createEventos linha 90'#Avaluo.objects.get(FolioK=event['title'])
        insert_id = Booking(None, event['start'], event['end'], event['allDay'], avaluo.avaluo_id, request.user.id, '')
        insert_id.save()
        obj = Booking.objects.latest('booking_id')
        output['id'] = obj.booking_id

    # Output in JSON
    outputStr = simplejson.dumps(output)
    return HttpResponse(outputStr)


@csrf_exempt
def cargaEventos(request):
    start = request.POST.get("start", "")
    end = request.POST.get("end", "")
    bookings = Booking.objects.filter(Inicio__gte=start, Fin__lte=end)

    data = {}
    bookings_json = []
    for e in bookings:
        data['id'] = int(e.booking_id)
        data['title'] = str(e.avaluo.FolioK) + " - " + smart_str(e.avaluo.Colonia)
        data['start'] = e.Inicio.strftime("%Y-%m-%dT%H:%M:%S")
        data['end'] = e.Fin.strftime("%Y-%m-%dT%H:%M:%S")
        data['allDay'] = e.diaEntero
        if e.visita:
            data['visitador'] = e.visita.id
            user_prof = 1 #UserProfile.objects.filter(user_id=e.visita.id).first()
            if user_prof:
                data['color'] = user_prof.color
        bookings_json.append(data)
        data = {}
    return HttpResponse(simplejson.dumps(bookings_json))


@csrf_exempt
def eliminaEventos(request):
    output = {}
    record_id = request.POST.get("id", "")
    if(record_id is not None and record_id != ''):
        event_id = Booking.objects.get(booking_id=record_id)
        event_id.delete()
        output['id'] = record_id
    return HttpResponse(record_id)


@csrf_exempt
def actualizaVisitador(request):
    output = {}
    record_id = request.POST.get("id", "")
    visitador_id = request.POST.get("visitador_id", "")
    if(record_id is not None and record_id != ''):
        event_id = Booking.objects.filter(booking_id=record_id)
        event_id.update(visita=visitador_id)

        output['id'] = record_id
    return HttpResponse(record_id)
