# from django.contrib.auth.models import User
from rest_framework import serializers

from vitrinebela.accounts.models import User
from vitrinebela.bookings.models import Booking


class BookingSerializer(serializers.HyperlinkedModelSerializer):

    user = serializers.PrimaryKeyRelatedField(
        read_only=False,
        queryset=User.objects.all()
    )

    class Meta:
        model = Booking
        fields = ('user', 'title', 'start', 'end','created_on', 'authorized', 'color')
