from rest_framework import serializers
from servers.models import Server, Metric, Incident
from django.utils import timezone

class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = "__all__"

class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = "__all__"

    def validate(self, data):
        percentage_fields = [
            "cpu_usage",
            "memory_usage",
            "disk_usage",
        ]

        for field in percentage_fields:
            value = data.get(field)

            if value is not None and not 0 <= value <= 100:
                raise serializers.ValidationError({
                    field: "O valor deve estar entre 0 e 100."
                })

        uptime = data.get("uptime")

        if uptime is not None and uptime < 0:
            raise serializers.ValidationError({
                "uptime": "O uptime não pode ser negativo."
            })

        return data

    def create(self, validated_data):
        metric = Metric.objects.create(**validated_data)

        metric.server.status = "online"
        metric.server.last_seen = timezone.now()

        metric.server.save(
            update_fields=["status", "last_seen"]
        )

        checks = [
            ("cpu_usage", metric.cpu_usage, 90, "high"),
            ("memory_usage", metric.memory_usage, 90, "high"),
            ("disk_usage", metric.disk_usage, 90, "critical"),
        ]

        for resource, value, limit, severity in checks:
            if value > limit:
                Incident.objects.create(
                    server=metric.server,
                    description=(
                        f"Utilização de {resource} elevada: "
                        f"{value}% (limite: {limit}%)."
                    ),
                    severity=severity,
                )

        return metric

class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = "__all__"

