from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from BeautyBarterAPI.models import Barter, Member, Service

class BarterView(ViewSet):

    def retrieve(self, request, pk):
        """Handle GET requests for single barter

        Returns:
            Response -- JSON serialized barter instance
        """
        try:
            barter = Barter.objects.get(pk=pk)
            serializer = BarterSerializer(barter, context={'request': request})
            return Response(serializer.data)
        
        except Barter.DoesNotExist as ex:
            return Response({'message': 'Barter does not exist'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return HttpResponseServerError(ex) 

    def list(self, request):
        """Handle GET requests to get all barters

        Returns:
            Response -- JSON serialized list of barters
        """
        barters = Barter.objects.all()
        serializer = BarterSerializer(barters, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns
        Response -- JSON serialized barter instance
        """
        member = Member.objects.get(user=request.auth.user)

        barter = Barter()

        try:
            barter.date_posted = request.data["date_posted"]
            barter.requested_details = request.data["requested_details"]
            barter.offered_details = request.data["offered_details"]
            barter.includes_product = request.data["includes_product"]
        
        except KeyError as ex:
            return Response({'message': 'Incorrect key was sent in request'}, status=status.HTTP_400_BAD_REQUEST)
        
        barter.member = member

        try:
            requested = Service.objects.get(pk=request.data["service_requested"])
            barter.service_requested = requested
        
        except Service.DoesNotExist as ex:
            return Response({'message': 'Service provided is not valid'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            offered = Service.objects.get(pk=request.data["service_offered"])
            barter.service_offered = offered
        
        except Service.DoesNotExist as ex:
            return Response({'message': 'Service provided is not valid'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            barter.save()
            serializer = BarterSerializer(barter, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ex:
            return Response({"reason": "You passed some bad data"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests for a barter

        Returns:
        Response -- Empty body with 204 status code
        """
        member = Member.objects.get(user=request.auth.user)

        barter = Barter.objects.get(pk=pk)
        barter.date_posted = request.data["date_posted"]
        barter.requested_details = request.data["requested_details"]
        barter.offered_details = request.data["offered_details"]
        barter.includes_product = request.data["includes_product"]
        barter.member = member

        try:
            requested = Service.objects.get(pk=request.data["service_requested"])
            barter.service_requested = requested

            barter.save()
        
        except ValueError:
            return Response({"reason": "You passed some bad data"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            offered = Service.objects.get(pk=request.data["service_offered"])
            barter.service_offered = offered

            barter.save()
        
        except ValueError:
            return Response({"reason": "You passed some bad data"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a barter

        Returns:
        Response -- Empty body with 204, 404, 500 status code
        """
        try:
            barter = Barter.objects.get(pk=pk)
            barter.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        except Barter.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('id', 'username',)

class ServiceRequestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('id', 'category', 'service', 'cost', 'per',)

class ServiceOfferedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('id', 'category', 'service', 'cost', 'per',)

class BarterSerializer(serializers.ModelSerializer):
    """JSON serializer for bourbons
    """
    member = MemberSerializer(many=False)
    service_requested = ServiceRequestedSerializer(many=False)
    service_offered = ServiceOfferedSerializer(many=False)
    class Meta:
        model = Barter
        fields = ('id', 'date_posted', 'requested_details', 'offered_details', 'includes_product', 'service_requested', 'service_offered', 'member',)
        depth = 1
