from django.db import models

class Server(models.Model):
    name = models.CharField(max_length=100)
    hostname = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    operating_system = models.CharField(max_length=100)

    status = models.CharField(
        max_length=20,
        default="offline"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class Metric(models.Model):
    server = models.ForeignKey(
        Server,
        on_delete=models.CASCADE,
        related_name="metrics"
    )

    cpu_usage = models.FloatField()
    memory_usage = models.FloatField()
    disk_usage = models.FloatField()
    uptime = models.FloatField()

    collected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Métricas de {self.server.name} - {self.collected_at}"


class Incident(models.Model):
    SEVERITY_CHOICES = [
        ("low", "Baixa"),
        ("medium", "Média"),
        ("high", "Alta"),
        ("critical", "Crítica"),
    ]

    server = models.ForeignKey(
        Server,
        on_delete=models.CASCADE,
        related_name="incidents"
    )

    description = models.TextField()
    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES,
        default="low"
    )

    resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.severity}: {self.server.name}"
