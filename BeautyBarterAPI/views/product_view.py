from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from BeautyBarterAPI.models import Product, ProductType
from django.contrib.auth.models import User

class ProductView(ViewSet):

    def retrieve(self, request, pk):
        """Handle GET requests for single product

        Returns:
            Response -- JSON serialized product instance
        """
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product, context={'request': request})
            return Response(serializer.data)
        
        except Product.DoesNotExist as ex:
            return Response({'message': 'Product does not exist'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return HttpResponseServerError(ex) 

    def list(self, request):
        """Handle GET requests to get all products

        Returns:
            Response -- JSON serialized list of products
        """
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns
        Response -- JSON serialized product instance
        """
        added_by = User.objects.get(user=request.auth.user)

        product = Product()

        try:
            product.name = request.data["name"]
            product.instructions = request.data["instructions"]
            product.cost = request.data["cost"]
        
        except KeyError as ex:
            return Response({'message': 'Incorrect key was sent in request'}, status=status.HTTP_400_BAD_REQUEST)
        
        product.added_by = added_by

        try:
            category = ProductType.objects.get(pk=request.data["product_category"])
            product.product_category = category
        
        except ProductType.DoesNotExist as ex:
            return Response({'message': 'Product category provided is not valid'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            product.save()
            serializer = ProductSerializer(product, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ex:
            return Response({"reason": "You passed some bad data"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests for a product

        Returns:
        Response -- Empty body with 204 status code
        """
        added_by = User.objects.get(user=request.auth.user)

        product = Product.objects.get(pk=pk)
        product.name = request.data["name"]
        product.instructions = request.data["instructions"]
        product.cost = request.data["cost"]
        product.added_by = added_by

        try:
            category = ProductType.objects.get(pk=request.data["product_category"])
            product.product_category = category

            product.save()
        
        except ValueError:
            return Response({"reason": "You passed some bad data"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a product

        Returns:
        Response -- Empty body with 204, 404, 500 status code
        """
        try:
            product = Product.objects.get(pk=pk)
            product.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username',)

class BourbonTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ('id', 'category',)

class ProductSerializer(serializers.ModelSerializer):
    """JSON serializer for products
    """
    added_by = UserSerializer(many=False)
    product_category = BourbonTypeSerializer(many=False)
    class Meta:
        model = Product
        fields = ('id', 'name', 'instructions', 'cost', 'product_category', 'added_by',)
        depth = 1
