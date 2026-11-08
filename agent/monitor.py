
import os
import time
import socket
import platform

import psutil
import requests


API_URL = "http://127.0.0.1:8000"
SERVER_ID = 1
INTERVAL = 30


def collect_metrics():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    uptime = time.time() - psutil.boot_time()

    return {
        "server": SERVER_ID,
        "cpu_usage": cpu,
        "memory_usage": memory,
        "disk_usage": disk,
        "uptime": uptime,
    }


def send_metrics(metrics):
    try:
        response = requests.post(
            f"{API_URL}/metrics/",
            json=metrics,
            timeout=10,
        )

        response.raise_for_status()

        print("[OK] Métricas enviadas com sucesso.")

    except requests.RequestException as error:
        print(f"[ERRO] Falha ao enviar métricas: {error}")


def main():
    print("Linux Server Monitor iniciado!")
    print(f"Hostname: {socket.gethostname()}")
    print(f"Sistema: {platform.system()} {platform.release()}")

    while True:
        metrics = collect_metrics()

        print(f"CPU: {metrics['cpu_usage']}%")
        print(f"RAM: {metrics['memory_usage']}%")
        print(f"Disco: {metrics['disk_usage']}%")

        send_metrics(metrics)

        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
