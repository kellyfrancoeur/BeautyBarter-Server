from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from BeautyBarterAPI.models import Member, Notification, NotificationType, PotentialBarter
from datetime import datetime


class NotificationView(ViewSet):

    def list(self, request):

        logged_in_member = Member.objects.get(pk=request.auth.member.id)

        notifications = Notification.objects.filter(
            receiver=logged_in_member.pk, viewed=False
        ).order_by("date_created")

        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
    
        potential_barter = PotentialBarter()

        requesting_member = Member.objects.get(pk=request.auth.member.id)
        potential_barter.member_requesting = requesting_member
        requested_member = Member.objects.get(pk=request.query_params['member_requested'])
        potential_barter.member_requested = requested_member
        potential_barter.date_requested = datetime.today()
        potential_barter.save()

        notification = Notification()
        notification.receiver = requested_member
        notification.sender = requesting_member
        notification.date_created = datetime.today()
        notification.viewed = False
        notification.notification_type = NotificationType.objects.get(pk=request.data["notification_type"])
        notification.save()

        serializer = NotificationSerializer(notification)
        return Response(serializer.data)

    def update(self, request, pk):
        needed_notification = Notification.objects.get(pk=pk)
        needed_notification.viewed = request.data["viewed"]
        needed_notification.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        notification = Notification.objects.get(pk=pk)
        notification.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class MemberSerializer(serializers.ModelSerializer):
    class Meta:

        model = Member
        fields = ('id', 'username')


class NotificationTypeSerializer(serializers.ModelSerializer):
    class Meta:

        model = NotificationType
        fields = ('id', 'type')


class NotificationSerializer(serializers.ModelSerializer):

    sender = MemberSerializer(many=False)
    receiver = MemberSerializer(many=False)
    notification_type = NotificationTypeSerializer(many=False)

    class Meta:
        model = Notification
        fields = ('id', 'receiver', 'sender', 'date_created', 'viewed',
                  'notification_type')