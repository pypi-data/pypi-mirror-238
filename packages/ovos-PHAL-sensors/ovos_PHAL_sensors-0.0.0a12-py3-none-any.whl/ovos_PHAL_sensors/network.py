import dataclasses
import urllib

from ovos_utils import classproperty

from ovos_PHAL_sensors.base import Sensor


@dataclasses.dataclass
class ExternalIPSensor(Sensor):
    unique_id: str = "external_ip"
    device_name: str = "network"
    _ip = "0.0.0.0"

    @property
    def value(self):
        try:
            self._ip = urllib.request.urlopen('https://api.ipify.org').read().decode('utf8')
        except:
            pass
        return self._ip

    @property
    def attrs(self):
        return {"friendly_name": self.__class__.__name__,
                "icon": "mdi:ip"}


if __name__ == "__main__":
    print(ExternalIPSensor())
    # external_ip(89.155.204.43, string)
