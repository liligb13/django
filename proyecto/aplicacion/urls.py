from django.urls import path,include
from aplicacion.viewsets import SensorViewSet, MedicionViewSet
from aplicacion import views
from rest_framework import routers

router=routers.DefaultRouter()
router.register(r'sensores',SensorViewSet) 
router.register(r'mediciones',MedicionViewSet) 

urlpatterns=[
    path('',include(router.urls)),
    # Endpoint for Arduino devices (POST sensor readings by serial): /rest/arduino/
    path('arduino/', views.arduino_data),
]