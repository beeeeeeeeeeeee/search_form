from rest_framework import serializers
from search.models import Product

# Serializers define the API representation.
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['pid', 'brand', 'model', 'submodel', 'colour', 'type']