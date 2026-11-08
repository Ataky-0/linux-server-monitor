from rest_framework import viewsets

from servers.models import Server, Metric, Incident
from servers.api.serializers import (
    ServerSerializer,
    MetricSerializer,
    IncidentSerializer,
)


class ServerViewSet(viewsets.ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer


class MetricViewSet(viewsets.ModelViewSet):
    queryset = Metric.objects.all()
    serializer_class = MetricSerializer


class IncidentViewSet(viewsets.ModelViewSet):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer

