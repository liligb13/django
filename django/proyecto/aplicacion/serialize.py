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


class ArduinoDataSerializer(serializers.Serializer):
    """Serializer to validate Arduino JSON payloads.

    Expected payload example:
        {
            "serial": "ABC123456789",
            "valor": 12.34,
            "fecha_hora": "2025-11-27T10:12:00Z"  # optional
        }
    """
    serial = serializers.CharField(max_length=50)
    valor = serializers.FloatField()
    fecha_hora = serializers.DateTimeField(required=False)