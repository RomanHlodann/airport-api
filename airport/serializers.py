from rest_framework import serializers

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


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city")


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class RouteListSerializer(serializers.ModelSerializer):
    source_closest_big_city = serializers.CharField(
        source="source.closest_big_city"
    )
    destination_closest_big_city = serializers.CharField(
        source="destination.closest_big_city"
    )

    class Meta:
        model = Route
        fields = ("id",  "source_closest_big_city",
                  "destination_closest_big_city", "distance")


class RouteDetailSerializer(RouteListSerializer):
    source_airport = serializers.CharField(source="source.name")
    destination_airport = serializers.CharField(source="destination.name")

    class Meta:
        model = Route
        fields = ("id", "source_airport", "source_closest_big_city",
                  "destination_airport", "destination_closest_big_city", "distance")
