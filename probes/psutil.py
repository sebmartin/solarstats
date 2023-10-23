from probes import Probe
import psutil


class PSUtil(Probe):
    def version(self) -> str:
        return "0.1"

    def poll(self) -> dict:
        return {
            "virtual_memory": psutil.virtual_memory()._asdict(),
            "cpu_count": psutil.cpu_count(),
            "cpu_percent": psutil.cpu_percent(percpu=False),
            "cpu_percents": psutil.cpu_percent(percpu=True),
            "disk_usage": psutil.disk_usage('/')._asdict(),
            "sensors_temperatures": {
                key: [
                    temp._asdict() for temp in temps
                ]
                for key, temps in psutil.sensors_temperatures().items()
            },
        }