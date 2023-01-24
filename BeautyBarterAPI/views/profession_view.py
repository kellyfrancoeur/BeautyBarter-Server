from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from BeautyBarterAPI.models import Profession, Admin

class ProfessionView(ViewSet):

    def retrieve(self, request, pk):
        """Handle GET requests for single profession

        Returns:
            Response -- JSON serialized profession instance
        """
        try:
            profession = Profession.objects.get(pk=pk)
            serializer = ProfessionSerializer(profession, context={'request': request})
            return Response(serializer.data)
        
        except Profession.DoesNotExist as ex:
            return Response({'message': 'Profession does not exist'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return HttpResponseServerError(ex) 

    def list(self, request):
        """Handle GET requests to get all professions

        Returns:
            Response -- JSON serialized list of professions
        """
        professions = Profession.objects.all()
        serializer = ProfessionSerializer(professions, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns
        Response -- JSON serialized profession instance
        """
        admin = Admin.objects.get(user=request.auth.user)

        profession = Profession()

        try:
            profession.profession = request.data["profession"]
        
        except KeyError as ex:
            return Response({'message': 'Incorrect key was sent in request'}, status=status.HTTP_400_BAD_REQUEST)
        
        profession.admin = admin
        
        try:
            profession.save()
            serializer = ProfessionSerializer(profession, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ex:
            return Response({"reason": "You passed some bad data"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests for a profession

        Returns:
        Response -- Empty body with 204 status code
        """
        admin = Admin.objects.get(user=request.auth.user)

        profession = Profession.objects.get(pk=pk)
        profession.profession = request.data["profession"]
        profession.admin = admin

        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a profession

        Returns:
        Response -- Empty body with 204, 404, 500 status code
        """
        try:
            profession = Profession.objects.get(pk=pk)
            profession.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        except Profession.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ('id', 'username',)

class ProfessionSerializer(serializers.ModelSerializer):
    """JSON serializer for professions
    """
    admin = AdminSerializer(many=False)

    class Meta:
        model = Profession
        fields = ('id', 'profession', 'admin',)
        depth = 1
