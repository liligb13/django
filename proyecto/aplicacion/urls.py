from django.urls import path,include
from aplicacion.viewsets import SensorViewSet, MedicionViewSet
from rest_framework import routers

router=routers.DefaultRouter()
router.register(r'sensores',SensorViewSet) 
router.register(r'mediciones',MedicionViewSet) 

urlpatterns=[
    path('',include(router.urls))  
]