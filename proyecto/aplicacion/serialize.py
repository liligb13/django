from rest_framework import serializers
from aplicacion.models import Sensor,Medicion

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'
        
class MedicionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicion
        fields = '__all__'  