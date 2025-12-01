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
            "serial": "ARDUINO1",
            "valor": 25.5,
            "tipo": "T",  # 'T' for temperature, 'H' for humidity
            "fecha_hora": "2025-11-27T10:12:00Z"  # optional
        }
    """
    serial = serializers.CharField(max_length=50)
    valor = serializers.FloatField()
    tipo = serializers.ChoiceField(
        choices=Medicion.TIPO_CHOICES, 
        default=Medicion.TEMPERATURA,
        required=False
    )
    fecha_hora = serializers.DateTimeField(required=False)