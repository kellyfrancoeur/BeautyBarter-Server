from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from BeautyBarterAPI.models import Message, Member
from django.db.models import Q
from datetime import datetime


class MessageView(ViewSet):

    def retrieve(self, request, pk):

        message = Message.objects.get(pk=pk)
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):

        messages = []
        if "sender" in request.query_params and "recipient" in request.query_params:
            sender_id = request.query_params['sender']
            member2_id = request.query_params['recipient']
            sender = Member.objects.get(pk=sender_id)
            recipient = Member.objects.get(pk=member2_id)
            messages = Message.objects.filter(
                Q(recipient_id=sender.user_id) & Q(sender_id=recipient.user_id)
            ) | Message.objects.filter(
                Q(recipient_id=recipient.user_id) & Q(sender_id=sender.user_id)
            ).order_by("date_time")

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        new_message = Message()

        new_message.sender = request.auth.user
        needed_recipient = Member.objects.get(pk=request.data["recipient"])
        new_message.recipient = needed_recipient
        new_message.date_time = datetime.today()
        new_message.content = request.data["content"]
        new_message.save()

        serializer = MessageSerializer(new_message)
        return Response(serializer.data)


class SenderSerializer(serializers.ModelSerializer):
    class Meta:

        model = Member
        fields = ('id', 'username')


class MessageSerializer(serializers.ModelSerializer):

    sender = SenderSerializer(many=False)

    class Meta:
        model = Message
        fields = ('id', 'sender', 'recipient', 'date_time',
                  'content')