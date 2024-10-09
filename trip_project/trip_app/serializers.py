from .models import Trip
from rest_framework import serializers

class TripSerializers(serializers.ModelSerializer):
    Trip_img = serializers.ImageField(required=False)

    class Meta:
        model = Trip
        fields = '__all__'  # Ensure this is correctly written
