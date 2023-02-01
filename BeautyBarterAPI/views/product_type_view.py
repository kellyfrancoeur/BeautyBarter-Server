from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from BeautyBarterAPI.models import ProductType, Profession


class ProductTypeView(ViewSet):

    def retrieve(self, request, pk):

        product_type = ProductType.objects.get(pk=pk)
        serializer = ProductTypeSerializer(product_type)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ('id', 'profession',)

class ProductTypeSerializer(serializers.ModelSerializer):

    category = ProfessionSerializer()
    class Meta:
        model = ProductType
        fields = ('id', 'category', 'type',)