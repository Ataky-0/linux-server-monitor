import pytest
from rest_framework.test import APIClient

from servers.models import Server, Metric, Incident


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def server():
    return Server.objects.create(
        name="Servidor de Teste",
        hostname="test-server",
        ip_address="192.168.1.100",
        operating_system="Arch Linux",
        status="offline",
    )


@pytest.mark.django_db
def test_create_server(api_client):
    response = api_client.post(
        "/servers/",
        {
            "name": "Servidor Teste",
            "hostname": "test-server",
            "ip_address": "192.168.1.100",
            "operating_system": "Arch Linux",
            "status": "offline",
        },
        format="json",
    )

    assert response.status_code == 201
    assert Server.objects.count() == 1


@pytest.mark.django_db
def test_list_servers(api_client, server):
    response = api_client.get("/servers/")

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["name"] == "Servidor de Teste"


@pytest.mark.django_db
def test_update_server(api_client, server):
    response = api_client.patch(
        f"/servers/{server.id}/",
        {"name": "Servidor Atualizado"},
        format="json",
    )

    assert response.status_code == 200

    server.refresh_from_db()
    assert server.name == "Servidor Atualizado"


@pytest.mark.django_db
def test_reject_invalid_metric(api_client, server):
    response = api_client.post(
        "/metrics/",
        {
            "server": server.id,
            "cpu_usage": 150,
            "memory_usage": 50,
            "disk_usage": 60,
            "uptime": 3600,
        },
        format="json",
    )

    assert response.status_code == 400
    assert Metric.objects.count() == 0


@pytest.mark.django_db
def test_create_incident_automatically(api_client, server):
    response = api_client.post(
        "/metrics/",
        {
            "server": server.id,
            "cpu_usage": 95,
            "memory_usage": 50,
            "disk_usage": 60,
            "uptime": 3600,
        },
        format="json",
    )

    assert response.status_code == 201
    assert Metric.objects.count() == 1
    assert Incident.objects.count() == 1
    assert Incident.objects.first().severity == "high"

