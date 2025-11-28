from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from aplicacion.models import Sensor, Medicion
import json


class ArduinoEndpointTests(TestCase):
	def setUp(self):
		# create a sensor that the Arduino will refer to using serial
		self.sensor = Sensor.objects.create(
			serial='ARDUINO12345A',
			nombre='Sensor Prueba',
			descripcion='para test',
			modelo='X1',
			fabricante='ACME',
			fecha_compra=timezone.now().date(),
			activo=True,
		)

	def test_post_arduino_creates_medicion(self):
		url = '/rest/arduino/'
		payload = {'serial': self.sensor.serial, 'valor': 12.5}
		resp = self.client.post(url, data=json.dumps(payload), content_type='application/json')
		self.assertEqual(resp.status_code, 201)
		self.assertEqual(Medicion.objects.count(), 1)
		m = Medicion.objects.first()
		self.assertAlmostEqual(m.valor, 12.5)
		self.assertEqual(m.sensor, self.sensor)

	def test_post_arduino_missing_sensor_returns_404(self):
		url = '/rest/arduino/'
		payload = {'serial': 'UNKNOWN000000', 'valor': 1.0}
		resp = self.client.post(url, data=json.dumps(payload), content_type='application/json')
		self.assertEqual(resp.status_code, 404)


class DefaultSensorBehaviorTest(TestCase):
	def test_post_with_default_serial_creates_sensor_and_medicion(self):
		# POSTing with the default ARDUINO1 serial should auto-create the sensor and save a measurement
		url = '/rest/arduino/'
		payload = {'serial': 'ARDUINO1', 'valor': 5.5}
		resp = self.client.post(url, data=json.dumps(payload), content_type='application/json')
		self.assertEqual(resp.status_code, 201)
		from aplicacion.models import Sensor, Medicion
		self.assertTrue(Sensor.objects.filter(serial='ARDUINO1').exists())
		self.assertEqual(Medicion.objects.count(), 1)
