from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from BeautyBarterAPI.models import LicenseState, Admin

class LicenseStateView(ViewSet):

    def retrieve(self, request, pk):
        """Handle GET requests for single state

        Returns:
            Response -- JSON serialized state instance
        """
        try:
            state = LicenseState.objects.get(pk=pk)
            serializer = LicenseStateSerializer(state, context={'request': request})
            return Response(serializer.data)
        
        except LicenseState.DoesNotExist as ex:
            return Response({'message': 'State does not exist'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return HttpResponseServerError(ex) 

    def list(self, request):
        """Handle GET requests to get all states

        Returns:
            Response -- JSON serialized list of states
        """
        states = LicenseState.objects.all()
        serializer = LicenseStateSerializer(states, many=True)
        return Response(serializer.data)

class LicenseStateSerializer(serializers.ModelSerializer):
    """JSON serializer for states
    """

    class Meta:
        model = LicenseState
        fields = ('id', 'state',)
