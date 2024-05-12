from rest_framework import viewsets

from airport.models import (
    Airport,
    Route,
    Crew,
    AirplaneType,
    Airplane,
    Flight,
    Order,
    Ticket
)
from airport.serializers import (
    AirportSerializer,
    RouteSerializer,
    RouteListSerializer,
    RouteDetailSerializer,
    CrewSerializer,
    AirplaneTypeSerializer,
    AirplaneSerializer,
    AirplaneListSerializer,
    FlightSerializer,
    FlightListSerializer,
    FlightDetailSerializer
)


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related("source", "destination")
    serializer_class = RouteSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        if self.action == "retrieve":
            return RouteDetailSerializer
        return self.serializer_class


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.select_related("airplane_type")
    serializer_class = AirplaneSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer
        return self.serializer_class


class FlightViewSet(viewsets.ModelViewSet):
    queryset = (Flight.objects.select_related("airplane")
                .prefetch_related("crew"))
    serializer_class = FlightSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action == "retrieve":
            queryset.select_related("airplane__airplane_type")
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        if self.action == "retrieve":
            return FlightDetailSerializer
        return self.serializer_class
