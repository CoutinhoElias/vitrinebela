from django.contrib.auth.models import User
#from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from vitrinebela.bookings.models import Booking


class BookingCreateUpdateSerializer(ModelSerializer):

    # user = serializers.PrimaryKeyRelatedField(
    #     read_only=False,
    #     queryset=User.objects.all()
    # )

    class Meta:
        model = Booking
        fields = ('id',
                  'user',
                  'title',
                  'start',
                  'end',
                  'created_on',
                  'authorized',
                  'color')


class BookingListSerializer(ModelSerializer):

    # user = serializers.PrimaryKeyRelatedField(
    #     read_only=False,
    #     queryset=User.objects.all()
    # )

    class Meta:
        model = Booking
        fields = ('id',
                  'user',
                  'title',
                  'start',
                  'end',
                  'created_on',
                  'authorized',
                  'color')


class BookingDetailSerializer(ModelSerializer):

    # user = serializers.PrimaryKeyRelatedField(
    #     read_only=False,
    #     queryset=User.objects.all()
    # )

    class Meta:
        model = Booking
        fields = ('id',
                  'user',
                  'title',
                  'start',
                  'end',
                  'created_on',
                  'authorized',
                  'color')
