from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from aplicacion.models import Sensor, Medicion
from django.utils import timezone
from aplicacion.serialize import ArduinoDataSerializer, MedicionSerializer


@api_view(['POST'])
def arduino_data(request):
    """Endpoint used by Arduino (or gateway) to post sensor readings.

    Expects JSON body with 'serial' and 'valor' (float), optional 'fecha_hora' and 'tipo'.
    Creates a Medicion associated with the Sensor whose serial matches.
    """
    serializer = ArduinoDataSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serial = serializer.validated_data['serial']
    valor = serializer.validated_data['valor']
    fecha_hora = serializer.validated_data.get('fecha_hora')
    tipo = serializer.validated_data.get('tipo', Medicion.TEMPERATURA)  # Default to temperature

    try:
        sensor = Sensor.objects.get(serial=serial)
    except Sensor.DoesNotExist:
        # If the incoming serial equals the default expected sensor for Arduino 1
        # create the DHT11 sensor automatically so a single device is always available.
        DEFAULT_SERIAL = 'ARDUINO1'
        if serial == DEFAULT_SERIAL:
            sensor = Sensor.objects.create(
                serial=DEFAULT_SERIAL,
                nombre='DHT11 Arduino 1',
                descripcion='Sensor DHT11 (autocreado para Arduino 1)',
                modelo='DHT11',
                fabricante='Generic',
                fecha_compra=timezone.now().date(),
                activo=True,
            )
        else:
            return Response(
                {'detail': 'Sensor no encontrado con el serial proporcionado.'}, 
                status=status.HTTP_404_NOT_FOUND
            )

    # Create the measurement
    medicion_data = {
        'sensor': sensor.id,
        'valor': valor,
        'tipo': tipo
    }
    if fecha_hora:
        medicion_data['fecha_hora'] = fecha_hora

    medicion_serializer = MedicionSerializer(data=medicion_data)
    if medicion_serializer.is_valid():
        medicion_serializer.save()
        return Response(medicion_serializer.data, status=status.HTTP_201_CREATED)
    return Response(medicion_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LatestReadingsView(generics.ListAPIView):
    """
    Vista para obtener las últimas lecturas de temperatura y humedad.
    """
    serializer_class = MedicionSerializer

    def get_queryset(self):
        # Obtener la última lectura de temperatura
        latest_temp = Medicion.objects.filter(
            tipo=Medicion.TEMPERATURA
        ).order_by('-fecha_hora').first()
        
        # Obtener la última lectura de humedad
        latest_hum = Medicion.objects.filter(
            tipo=Medicion.HUMEDAD
        ).order_by('-fecha_hora').first()
        
        # Devolver ambas lecturas si existen
        readings = []
        if latest_temp:
            readings.append(latest_temp)
        if latest_hum:
            readings.append(latest_hum)
        return readings

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

