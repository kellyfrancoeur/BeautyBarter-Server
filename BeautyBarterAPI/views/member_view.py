from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from BeautyBarterAPI.models import Member, Profession, LicenseState, MemberPortfolioImages


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
        try:
            member = Member.objects.get(pk=pk)
            serializer = MemberSerializer(member, context={'request': request})
            return Response(serializer.data)
        
        except Member.DoesNotExist as ex:
            return Response({'message': 'Member does not exist'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return HttpResponseServerError(ex)

    
    def update(self, request, pk=None):
        """Handle PUT requests for a member

        Returns:
        Response -- Empty body with 204 status code
        """

        member = Member.objects.get(pk=pk)
        member.full_name = request.data["full_name"]
        member.username = request.data["username"]
        member.email = request.data["email"]
        member.license_number = request.data["license_number"]
        member.link_to_site = request.data["link_to_site"]
        member.about = request.data["about"]
        member.interested_in = request.data["interested_in"]
        member.willing_to_trade = request.data["willing_to_trade"]
        member.member_img = request.data["member_img"]

        try:
            profession = Profession.objects.get(pk=request.data["profession"])
            member.profession = profession

            member.save()
        
        except ValueError:
            return Response({"reason": "You passed some bad data"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            state = LicenseState.objects.get(pk=request.data["license_state"])
            member.license_state = state

            member.save()
        
        except ValueError:
            return Response({"reason": "You passed some bad data"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            portfolio = MemberPortfolioImages.objects.get(pk=request.data["portfolio_img"])
            member.portfolio_img = portfolio

            member.save()
        
        except ValueError:
            return Response({"reason": "You passed some bad data"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
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