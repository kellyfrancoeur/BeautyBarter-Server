from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from BeautyBarterAPI.models import Admin


class AdminView(ViewSet):
    """Beauty Barter admin view"""

    def list(self, request):
        """Handle GET requests to get all admin users

        Returns:
            Response -- JSON serialized list of admin users
        """

        admins = Admin.objects.all()
        serialized = AdminSerializer(admins, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single admin user

        Returns:
            Response -- JSON serialized admin user record
        """

        admin = Admin.objects.get(pk=pk)
        serialized = AdminSerializer(admin, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)


class AdminSerializer(serializers.ModelSerializer):
    """JSON serializer for Admin"""
    class Meta:
        model = Admin
        fields = ('id', 'username', 'email', 'full_name', 'position', 'admin_img',)