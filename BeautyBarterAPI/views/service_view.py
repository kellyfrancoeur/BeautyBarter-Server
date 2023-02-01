from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from BeautyBarterAPI.models import Service, Profession
from django.contrib.auth.models import User

class ServiceView(ViewSet):

    def retrieve(self, request, pk):
        """Handle GET requests for single service

        Returns:
            Response -- JSON serialized service instance
        """
        try:
            service = Service.objects.get(pk=pk)
            serializer = ServiceSerializer(service, context={'request': request})
            return Response(serializer.data)
        
        except Service.DoesNotExist as ex:
            return Response({'message': 'Service does not exist'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return HttpResponseServerError(ex) 

    def list(self, request):
        """Handle GET requests to get all services

        Returns:
            Response -- JSON serialized list of services
        """
        services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns
        Response -- JSON serialized service instance
        """
        created_by = User.objects.get(user=request.auth.user)

        service = Service()

        try:
            service.service = request.data["service"]
            service.cost = request.data["cost"]
            service.per = request.data["per"]
        
        except KeyError as ex:
            return Response({'message': 'Incorrect key was sent in request'}, status=status.HTTP_400_BAD_REQUEST)
        
        service.created_by = created_by

        try:
            category = Profession.objects.get(pk=request.data["category"])
            service.category = category
        
        except Profession.DoesNotExist as ex:
            return Response({'message': 'Service category provided is not valid'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            service.save()
            serializer = ServiceSerializer(service, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ex:
            return Response({"reason": "You passed some bad data"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests for a service

        Returns:
        Response -- Empty body with 204 status code
        """
        created_by = User.objects.get(user=request.auth.user)

        service = Service.objects.get(pk=pk)
        service.service = request.data["service"]
        service.per = request.data["per"]
        service.cost = request.data["cost"]
        service.created_by = created_by

        try:
            category = Profession.objects.get(pk=request.data["category"])
            service.category = category

            service.save()
        
        except ValueError:
            return Response({"reason": "You passed some bad data"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a service

        Returns:
        Response -- Empty body with 204, 404, 500 status code
        """
        try:
            service = Service.objects.get(pk=pk)
            service.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        except Service.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username',)

class BourbonTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ('id', 'category',)

class ServiceSerializer(serializers.ModelSerializer):
    """JSON serializer for services
    """
    created_by = UserSerializer(many=False)
    category = BourbonTypeSerializer(many=False)
    class Meta:
        model = Service
        fields = ('id', 'service', 'per', 'cost', 'category', 'created_by',)
        depth = 1
