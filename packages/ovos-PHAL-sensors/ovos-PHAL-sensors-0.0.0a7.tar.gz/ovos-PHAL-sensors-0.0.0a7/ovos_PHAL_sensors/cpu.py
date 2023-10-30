import dataclasses
import os

import psutil
from ovos_utils import classproperty

from ovos_PHAL_sensors.base import NumericSensor, PercentageSensor


@dataclasses.dataclass
class CPUCountSensor(NumericSensor):
    unit: str = "number"
    unique_id: str = "count"
    device_name: str = "cpu"
    _once: bool = True

    @classproperty
    def value(self):
        return os.cpu_count()


@dataclasses.dataclass
class CPUUsageSensor(PercentageSensor):
    unique_id: str = "usage_percent"
    device_name: str = "cpu"

    @classproperty
    def value(self):
        return psutil.cpu_percent(1)


@dataclasses.dataclass
class CPUTemperatureSensor(NumericSensor):
    unit: str = "°C"
    unique_id: str = "temperature"
    device_name: str = "cpu"

    @classproperty
    def value(self):
        return psutil.sensors_temperatures()['coretemp'][0].current

    @classproperty
    def attrs(cls):
        return {"friendly_name": cls.__name__,
                "unit_of_measurement": "°C"}


if __name__ == "__main__":
    print(CPUCountSensor())
    print(CPUUsageSensor())
    print(CPUTemperatureSensor())
    # cpu_count(16, number)
    # cpu_percent(1.7, %)
    # cpu_temperature(39.0, °C)
