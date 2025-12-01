from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from aplicacion.models import Sensor, Medicion
from django.utils import timezone
from aplicacion.serialize import ArduinoDataSerializer, MedicionSerializer


@api_view(['POST'])
def arduino_data(request):
	"""Endpoint used by Arduino (or gateway) to post sensor readings.

	Expects JSON body with 'serial' and 'valor' (float), optional 'fecha_hora'.
	Creates a Medicion associated with the Sensor whose serial matches.
	"""
	serializer = ArduinoDataSerializer(data=request.data)
	if not serializer.is_valid():
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	serial = serializer.validated_data['serial']
	valor = serializer.validated_data['valor']
	fecha_hora = serializer.validated_data.get('fecha_hora')

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
			return Response({'detail': 'Sensor no encontrado con el serial proporcionado.'}, status=status.HTTP_404_NOT_FOUND)

	# If fecha_hora is supplied set it explicitly, otherwise let the model default (timezone.now()) set it
	if fecha_hora:
		medicion = Medicion.objects.create(sensor=sensor, valor=valor, fecha_hora=fecha_hora)
	else:
		medicion = Medicion.objects.create(sensor=sensor, valor=valor)

	out = MedicionSerializer(medicion)
	return Response(out.data, status=status.HTTP_201_CREATED)

