from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from BeautyBarterAPI.models import Member


class MemberView(ViewSet):
    """Beauty Barter member view"""

    def list(self, request):
        """Handle GET requests to get all members

        Returns:
            Response -- JSON serialized list of members
        """

        members = Member.objects.all()
        serialized = MemberSerializer(members, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single member

        Returns:
            Response -- JSON serialized member record
        """

        member = Member.objects.get(pk=pk)
        serialized = MemberSerializer(member, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a member

        Returns:
        Response -- Empty body with 204 status code
        """

        member = Member.objects.get(pk=pk)
        member.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class MemberSerializer(serializers.ModelSerializer):
    """JSON serializer for Bourbon User"""
    class Meta:
        model = Member
        fields = ('id', 'username', 'email','full_name', 'profession', 'license_state', 'license_number', 'link_to_site', 'about', 'interested_in', 'willing_to_trade', 'member_img', 'portfolio_img',)