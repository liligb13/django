from django.db import models
from django.core.validators import RegexValidator,MinLengthValidator
from django.utils import timezone

HOMBRE='H'
MUJER ='M'
INDISTINTO='I'
GENERO_CHOICES=[
    (HOMBRE,'Hombre'),
    (MUJER, 'Mujer'),
    (INDISTINTO,'Prefiero no decirlo '),
]
serial_12_validador=RegexValidator(
    regex=r'^[A-Za-z0-9#_@%$]{12}$',
    message='El serial debe tener exactamente 12 caracteres:letras numeros'
)
telefono_validador=RegexValidator(
    regex=r'^[0-9]{10}$',
    message='El telefono debe tener exactamente 10 digitoos '
)
class Sensor(models.Model):
    serial=models.CharField(max_length=50,
                            unique=True,
                            validators=[serial_12_validador])
    
    nombre=models.CharField(max_length=100)
    descripcion=models.TextField(blank=True,null=True)
    modelo=models.CharField(max_length=50)
    fabricante=models.CharField(max_length=50)
    fecha_compra=models.DateField()
    activo=models.BooleanField(default=True)
    
    def __str__(self):
        return f"({self.serial}){self.nombre} {self.fabricante}{self.modelo}"


class Medicion(models.Model):
    sensor = models.ForeignKey('Sensor', on_delete=models.PROTECT, related_name='mediciones_sensor')
    fecha_hora = models.DateTimeField(default=timezone.now, editable=False)
    valor = models.FloatField()
    
    class Meta:
        ordering = ['-fecha_hora']
    
    def __str__(self):
        return f"{self.sensor.serial} - {self.valor}°C - {self.fecha_hora.strftime('%Y-%m-%d %H:%M')}"

