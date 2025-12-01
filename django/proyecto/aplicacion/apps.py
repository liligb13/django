from django.apps import AppConfig
from django.utils import timezone
import sys
from django.db.utils import OperationalError, ProgrammingError


class AplicacionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'aplicacion'

    # Ensure the project has a default DHT11 sensor record on startup.
    def ready(self):
        # Avoid creating objects when running migrations or makemigrations
        if any(arg in sys.argv for arg in ('makemigrations', 'migrate', 'shell', 'dbshell')):
            return

        try:
            Sensor = self.get_model('Sensor')
            DEFAULT_SERIAL = 'ARDUINO1'
            if not Sensor.objects.filter(serial=DEFAULT_SERIAL).exists():
                Sensor.objects.create(
                    serial=DEFAULT_SERIAL,
                    nombre='DHT11 Arduino 1',
                    descripcion='Sensor DHT11 por defecto para Arduino 1 (creado automáticamente)',
                    modelo='DHT11',
                    fabricante='Generic',
                    fecha_compra=timezone.now().date(),
                    activo=True,
                )
        except (OperationalError, ProgrammingError):
            # Database not ready yet (e.g., during migrations) — skip quietly
            pass
