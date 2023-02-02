from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from BeautyBarterAPI.models import Member, PotentialBarter, Member, Barter


class PotentialBarterView(ViewSet):

    def retrieve(self, request, pk):

        request = PotentialBarter.objects.get(pk=pk)
        serializer = RequestSerializer(request)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):

        if "member_requested" in request.query_params:
            member_id = request.query_params['member_requested']

            requests = PotentialBarter.objects.filter(
                member_requested=member_id
            ).order_by("date_requested")

        else:
            logged_in_member_requesting = Member.objects.get(user=request.auth.user)
            requests = PotentialBarter.objects.filter(
                member_requesting=logged_in_member_requesting).order_by("date_requested")

        serializer = RequestSerializer(requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        new_request = PotentialBarter()

        logged_in_member_requesting = Member.objects.get(user=request.auth.user)
        barter = Barter.objects.get(pk=request.data["barter"])

        new_request.member_requesting = logged_in_member_requesting
        requested_member = Member.objects.get(pk=request.data["member_requested"])
        new_request.barter = barter
        new_request.member_requested = requested_member
        new_request.accepted = False
        new_request.date_requested = request.data["date_requested"]
        new_request.date_accepted = request.data["date_accepted"]
        new_request.save()

        serializer = RequestSerializer(new_request)
        return Response(serializer.data)

    def update(self, request, pk):
        needed_request = PotentialBarter.objects.get(pk=pk)
        needed_request.accepted = request.data["accepted"]
        needed_request.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        resource = PotentialBarter.objects.get(pk=pk)
        resource.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class MemberSerializer(serializers.ModelSerializer):
    class Meta:

        model = Member
        fields = ('id', 'full_name')


class RequestSerializer(serializers.ModelSerializer):

    member_requested = MemberSerializer(many=False)

    class Meta:
        model = PotentialBarter
        fields = ('id', 'member_requested', 'accepted', 'date_accepted',
                  'date_requested', 'member_requesting')