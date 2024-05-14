from datetime import datetime

from django.db.models import F, Count
from rest_framework import viewsets, mixins, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response

from airport.permissions import IsAdminOrIfAuthenticatedReadOnly
from airport.models import (
    Airport,
    Route,
    Crew,
    AirplaneType,
    Airplane,
    Flight,
    Order
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
    AirplaneImageSerializer,
    FlightSerializer,
    FlightListSerializer,
    FlightDetailSerializer,
    OrderSerializer,
    OrderListSerializer
)


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly, )


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related("source", "destination")
    serializer_class = RouteSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        if self.action == "retrieve":
            return RouteDetailSerializer
        return self.serializer_class


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.select_related("airplane_type")
    serializer_class = AirplaneSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return AirplaneListSerializer
        if self.action == "upload_image":
            return AirplaneImageSerializer
        return self.serializer_class

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
        permission_classes=(IsAdminUser,),
    )
    def upload_image(self, request, pk=None):
        """Endpoint for uploading image to specific airplane"""
        airplane = self.get_object()
        serializer = self.get_serializer(airplane, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        """Retrieve the flights with filters"""
        queryset = (self.queryset.select_related("airplane")
                        .prefetch_related("crew"))
        if self.action == "list":
            queryset = queryset.annotate(
                tickets_available=(
                        F("airplane__rows") * F("airplane__seats_in_row")
                        - Count("tickets")
                )
            )
        if self.action == "retrieve":
            queryset = queryset.select_related("airplane__airplane_type")

        route_id = self.request.query_params.get("route")
        airplanes = self.request.query_params.get("airplanes")
        departure_time = self.request.query_params.get("departure_time")
        arrival_time = self.request.query_params.get("arrival_time")

        if route_id:
            queryset = queryset.filter(route_id=int(route_id))
        if airplanes:
            airplanes_ids = self._params_to_ints(airplanes)
            queryset = queryset.filter(airplane_id__in=airplanes_ids)
        if departure_time:
            date = datetime.strptime(departure_time, "%Y-%m-%d").date()
            queryset = queryset.filter(departure_time__date=date)
        if arrival_time:
            date = datetime.strptime(arrival_time, "%Y-%m-%d").date()
            queryset = queryset.filter(arrival_time__date=date)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        if self.action == "retrieve":
            return FlightDetailSerializer
        return self.serializer_class


class OrderPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Order.objects.prefetch_related(
        "tickets__flight__route", "tickets__flight__airplane"
    )
    serializer_class = OrderSerializer
    pagination_class = OrderPagination
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
