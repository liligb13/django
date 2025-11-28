from rest_framework import serializers
from aplicacion.models import Sensor,Medicion

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'
        
class MedicionSerializer(serializers.ModelSerializer):
    serial_sensor = serializers.CharField(write_only=True)
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
    serial = serializers.CharField(max_length=50)
    valor = serializers.FloatField()
    fecha_hora = serializers.DateTimeField(required=False)