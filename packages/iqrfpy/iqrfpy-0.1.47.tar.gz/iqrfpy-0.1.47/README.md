## What is iqrfpy?

iqrfpy is a library that provides a python API for interacting with the IQRF network
utilizing the [DPA framework](https://doc.iqrf.org/DpaTechGuide/) (DPA) or IQRF Gateway Daemon (Daemon) [JSON API](https://docs.iqrf.org/iqrf-gateway/user/daemon/api). Communication between a python runtime and the IQRF network is facilitated by transports.

For communication with Daemon, only the MQTT transport is implemented at this time.
However, this library provides an abstract transport class, allowing for custom communication implementations.

The library provides classes for serialization of requests and deserialization of responses to message class objects.

## Quick start

iqrfpy can be installed using the pip utility:

```bash
python3 -m pip install -U iqrfpy
```

Example use:
```python
from iqrfpy.transports.mqtt_transport import MqttTransport, MqttTransportParams
from iqrfpy.peripherals.coordinator.requests.bonded_devices import BondedDevicesRequest
from iqrfpy.peripherals.coordinator.responses.bonded_devices import BondedDevicesResponse

params = MqttTransportParams(
    host=..., # MQTT broker host
    port=..., # MQTT broker port
    client_id=..., # MQTT client ID
    request_topic=..., # Request topic that Daemon subscribes to
    response_topic=..., # Response topic that Daemon publishes responses to
    qos=1,
    keepalive=25
)
transport = MqttTransport(params=params, auto_init=True)

request = BondedDevicesRequest()
response: BondedDevicesResponse = transport.send_and_receive(request=request, timeout=10)

print(response.bonded)
```

The library also provides a single import solution for messages:
```python
from iqrfpy.transports.mqtt_transport import MqttTransport, MqttTransportParams
from iqrfpy.messages import CoordinatorBondedDevicesReq, CoordinatorBondedDevicesRsp

params = MqttTransportParams(
    host=..., # MQTT broker host
    port=..., # MQTT broker port
    client_id=..., # MQTT client ID
    request_topic=..., # Request topic that Daemon subscribes to
    response_topic=..., # Response topic that Daemon publishes responses to
    qos=1,
    keepalive=25
)
transport = MqttTransport(params=params, auto_init=True)

request = CoordinatorBondedDevicesReq()
response: CoordinatorBondedDevicesRsp = transport.send_and_receive(request=request, timeout=10)

print(response.bonded)
```

## Documentation

For more information, check out our [API reference](https://apidocs.iqrf.org/iqrfpy/latest/iqrfpy.html).
