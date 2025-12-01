from rest_framework import serializers
from aplicacion.models import Sensor, Medicion
from django.utils import timezone

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'
        
class MedicionSerializer(serializers.ModelSerializer):
    serial_sensor = serializers.CharField(write_only=True, required=False)
    sensor = SensorSerializer(read_only=True)

    class Meta:
        model = Medicion
        fields = ('id', 'serial_sensor', 'sensor', 'valor', 'fecha_hora')
        read_only_fields = ('fecha_hora', 'id')

    def create(self, validated_data):
        serial = validated_data.pop('serial_sensor')
        
        try:
            sensor_obj = Sensor.objects.get(serial=serial)
        except Sensor.DoesNotExist:
            raise serializers.ValidationError({"serial_sensor": f"El sensor con serial '{serial}' no existe."})
        medicion = Medicion.objects.create(sensor=sensor_obj, **validated_data)
        return medicion
    
class ArduinoDataSerializer(serializers.Serializer):
    """Serializer to validate Arduino JSON payloads.

    Expected payload example:
        {
            "serial": "ARDUINO1",
            "valor": 24.5,  # Temperatura en grados Celsius
            "fecha_hora": "2025-11-30T23:47:00-07:00"  # opcional
        }
    """
    serial = serializers.CharField(max_length=50, default='ARDUINO1')
    valor = serializers.FloatField()
    fecha_hora = serializers.DateTimeField(required=False, default=timezone.now)
    
    def validate_serial(self, value):
        # Aceptamos cualquier serial, no forzamos el formato estricto
        return value