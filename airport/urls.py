from django.urls import path, include
from rest_framework import routers

from airport.views import (
    AirportViewSet,
    RouteViewSet,
    CrewViewSet
)

router = routers.DefaultRouter()
router.register("all", AirportViewSet)
router.register("routes", RouteViewSet)
router.register("crew", CrewViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "airport_service"
