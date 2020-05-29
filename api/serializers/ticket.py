from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from track.models import Ticket, TicketReply


class TicketSerializer(ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'


class TicketSerializer(ModelSerializer):
    replies = SerializerMethodField()
    lookup_field = 'ticketNumber'

    class Meta:
        model = Ticket
        fields = '__all__'

    def get_replies(self, obj):
        if obj.any_children:
            return TicketSerializer(obj.any_children(), many=True).data