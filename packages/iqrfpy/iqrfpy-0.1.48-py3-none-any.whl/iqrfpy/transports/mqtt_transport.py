import json
import random
import string
import threading

from typing import Callable, List, Optional
from paho.mqtt.client import Client
from iqrfpy.enums.message_types import MessageType
from iqrfpy.exceptions import TransportNotConnectedError, MessageNotReceivedError, DpaRequestTimeoutError, \
    JsonRequestTimeoutError, UnsupportedMessageTypeError, JsonResponseNotSupportedError
from iqrfpy.response_factory import ResponseFactory
from iqrfpy.transports.itransport import ITransport
from iqrfpy.irequest import IRequest
from iqrfpy.iresponse import IResponse
from iqrfpy.confirmation import Confirmation
from iqrfpy.utils.dpa import IQMESH_TEMP_ADDR, BROADCAST_ADDR

__all__ = [
    'MqttTransportParams',
    'MqttTransport',
]


class MqttParamsError(Exception):
    """MQTT parameters error.

    Raised if MQTT parameter does not validate.
    """

    pass


class MqttTransportParams:
    """MQTT transport parameters class."""

    __slots__ = '_host', '_port', '_client_id', '_user', '_password', '_request_topic', '_response_topic', '_qos', \
        '_keepalive'

    def __init__(self, host: str = 'localhost', port: int = 1883, client_id: Optional[str] = None,
                 user: Optional[str] = None, password: Optional[str] = None, request_topic: Optional[str] = None,
                 response_topic: Optional[str] = None, qos: int = 1, keepalive: int = 60):
        """MQTT transport parameters constructor.

        Args:
            host (str): Broker hostname. (Defaults to 'localhost')
            port (int): Broker port. (Defaults to 1883)
            client_id (str, optional): Client ID. If no client ID is specified, a randomly generated one will be used.
            user (str, optional): Broker username.
            password (str, optional): Broker password.
            request_topic (str, optional): Topic to publish requests to.
            response_topic (str, optional): Topic to subscribe to for responses.
            qos (int): Quality of service. (Defaults to 1)
            keepalive (int): Keep alive interval. (Defaults to 60)
        """
        self._validate(port=port, qos=qos)
        self._host = host
        self._port = port
        self._client_id = client_id if client_id is not None else \
            ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16))
        self._user = user
        self._password = password
        self._request_topic = request_topic
        self._response_topic = response_topic
        self._qos = qos
        self._keepalive = keepalive

    def _validate(self, port: int, qos: int):
        """Validate transport parameters.

        Args:
            port (int): Port.
            qos (int): Quality of service.
        """
        self._validate_port(port)
        self._validate_qos(qos)

    @property
    def host(self) -> str:
        """:obj:`str`: Broker hostname.

        Getter and setter.
        """
        return self._host

    @host.setter
    def host(self, value: str):
        self._host = value

    @staticmethod
    def _validate_port(port: int):
        """Validate broker port number.

        Args:
            port (int): Broker port number.
        Raises:
            MqttParamsError: If port is less than 1024 and greater than 65535.
        """
        if not (1024 <= port <= 65535):
            raise MqttParamsError('Port value should be between 1024 and 65535.')

    @property
    def port(self) -> int:
        """:obj:`int`: Broker port.

        Getter and setter.
        """
        return self._port

    @port.setter
    def port(self, value: int):
        self._validate_port(value)
        self._port = value

    @property
    def client_id(self) -> str:
        """:obj:`str`: Client ID.

        Getter and setter.
        """
        return self._client_id

    @client_id.setter
    def client_id(self, value: str):
        self._client_id = value

    @property
    def user(self) -> Optional[str]:
        """:obj:`str` or :obj:`None`: Broker username.

        Getter and setter.
        """
        return self._user

    @user.setter
    def user(self, value: Optional[str]):
        self._user = value

    @property
    def password(self) -> Optional[str]:
        """:obj:`str` or :obj:`None`: Broker password.

        Getter and setter.
        """
        return self._password

    @password.setter
    def password(self, value: Optional[str]):
        self._password = value

    @property
    def request_topic(self) -> Optional[str]:
        """:obj:`str` or :obj:`None`: Topic to publish requests to.

        Getter and setter.
        """
        return self._request_topic

    @request_topic.setter
    def request_topic(self, value: str):
        self._request_topic = value

    @property
    def response_topic(self) -> Optional[str]:
        """:obj:`str` or :obj:`None`: Topic to subscribe to for responses.

        Getter and setter.
        """
        return self._response_topic

    @response_topic.setter
    def response_topic(self, value: str):
        self._response_topic = value

    @staticmethod
    def _validate_qos(qos: int):
        """Validate quality of service parameter.

        Args:
            qos (int): Quality of service.
        Raises:
            MqttParamsError: If qos is less than 0 or greater than 2.
        """
        if not (0 <= qos <= 2):
            raise MqttParamsError('QoS value should be between 0 and 2.')

    @property
    def qos(self) -> int:
        """:obj:`int`: Quality of service.

        Getter and setter.
        """
        return self._qos

    @qos.setter
    def qos(self, value: int):
        self._validate_qos(value)
        self._qos = value

    @property
    def keepalive(self) -> int:
        """:obj:`int`: Keep alive interval.

        Getter and setter.
        """
        return self._keepalive

    @keepalive.setter
    def keepalive(self, value: int):
        self._keepalive = value


class MqttTransport(ITransport):
    """MQTT transport class."""

    __slots__ = '_client', '_params', '_callback', '_global_request_timeout', '_cv', '_msg_ids', '_m_type', \
        '_response', '_dpa_timeout', '_received_timeout', '_unsupported'

    def __init__(self, params: MqttTransportParams, callback: Optional[Callable] = None, auto_init: bool = False,
                 global_request_timeout: Optional[float] = 5):
        """MQTT transport constructor.

        Args:
            params (MqttTransportParams): MQTT parameters.
            callback (Callable, optional): Callback to process responses.
            auto_init (bool): Initialize and establish connection automatically.
            global_request_timeout (float, optional): Request timeout, used if timeout is not explicitly
                passed to receive methods.
        """
        self._client: Optional[Client] = None
        self._params: MqttTransportParams = params
        self._callback: Optional[Callable] = callback
        self._global_request_timeout: float = global_request_timeout
        self._cv: threading.Condition = threading.Condition()
        self._sub_cv: threading.Condition = threading.Condition()
        self._msg_ids: List[str] = []
        self._m_type: Optional[MessageType] = None
        self._response: Optional[IResponse] = None
        self._dpa_timeout: Optional[float] = None
        self._received_timeout: bool = False
        self._unsupported: bool = False
        if auto_init:
            self.initialize()

    def initialize(self) -> None:
        """Initialize and establish MQTT connection.

        The method initializes MQTT client, sets callbacks, connects to broker and subscribes to response topic.
        """
        self._client = Client(self._params.client_id)
        self._client.on_connect = self._connect_callback
        self._client.on_message = self._message_callback
        self._client.on_subscribe = self._subscribe_callback
        if self._params.user is not None and self._params.password is not None:
            self._client.username_pw_set(self._params.user, self._params.password)
        self._client.connect(self._params.host, self._params.port)
        self._client.loop_start()
        with self._sub_cv:
            self._sub_cv.wait()

    def terminate(self, force: bool = False) -> None:
        """Terminate MQTT connection.

        Args:
            force (bool): Force terminate connection. (Defaults to False)
        """
        self._client.disconnect()
        self._client.loop_stop(force=force)

    def _connect_callback(self, client, userdata, flags, rc):
        """On connect callback.

        Subscribes to response topic upon establishing connection.
        """
        # pylint: disable=W0613
        if rc == 0:
            self._client.subscribe(self._params.response_topic, self._params.qos)

    def _subscribe_callback(self, client, userdata, mid, granted_qos):
        """On subscribe callback.

        Notifies topic subscription conditional variable.
        """
        # pylint: disable=W0613
        with self._sub_cv:
            self._sub_cv.notify()

    def _message_callback(self, client, userdata, message):
        """On message callback.

        Processes messages published to response topic.
        If a callback has been assigned, then the response is passed to the callback as well.
        """
        # pylint: disable=W0613
        payload = json.loads(message.payload.decode('utf-8'))
        try:
            response = ResponseFactory.get_response_from_json(payload)
        except MessageNotReceivedError as err:
            if err.msgid == self._msg_ids[0]:
                self._received_timeout = True
                with self._cv:
                    self._cv.notify()
            return
        except UnsupportedMessageTypeError as err:
            if err.msgid == self._msg_ids[0]:
                self._unsupported = True
                with self._cv:
                    self._cv.notify()
            return
        if len(self._msg_ids) > 0 and response.msgid == self._msg_ids[0] and response.mtype == self._m_type:
            self._msg_ids.pop(0)
            self._response = response
            with self._cv:
                self._cv.notify()
        if self._callback is not None:
            self._callback(response)

    def is_connected(self) -> bool:
        """Check if client is connected.

        Returns:
            bool: True if client is connected to broker, False otherwise
        """
        return self._client.is_connected()

    def send(self, request: IRequest) -> None:
        """Publish message to request topic.

        Args:
            request (IRequest): Request to publish.
        Raises:
            TransportNotConnectedError: If client is not connected to the broker.
        """
        self._response = None
        self._m_type = None
        self._dpa_timeout = None
        self._received_timeout = False
        self._unsupported = False
        if not self._client.is_connected():
            raise TransportNotConnectedError(f'MQTT client {self._params.client_id} not connected to broker.')
        self._client.publish(
            topic=self._params.request_topic,
            payload=json.dumps(request.to_json()),
            qos=self._params.qos
        )
        if request.nadr == 255:
            return
        self._dpa_timeout = request.dpa_rsp_time
        self._msg_ids.append(request.msgid)
        self._m_type = request.mtype

    def confirmation(self) -> Confirmation:
        """Return confirmation message.

        Daemon JSON API does not send confirmation messages separately.

        Raises:
            NotImplementedError: Confirmation not implemented.
        """
        raise NotImplementedError('Method not implemented.')

    def receive(self, timeout: Optional[float] = None) -> Optional[IResponse]:
        """Receive message synchronously.

        Args:
            timeout (float, optional): Time to wait for request to be processed and response sent.
                If not specified, :obj:`global_request_timeout` is used.
        Raises:
            DpaRequestTimeoutError: If DPA request timed out.
            JsonRequestTimeoutError: If JSON API response was received, but DPA request timed out, or if the JSON API
                response was not received within specified timeout.
            JsonResponseNotSupportedError: If JSON API response with expected message ID was received,
                but the response message type is not supported.
        """
        if len(self._msg_ids) == 0:
            return None
        timeout_to_use = timeout if timeout is not None else self._global_request_timeout
        with self._cv:
            self._cv.wait(timeout=timeout_to_use)
        if self._response is None:
            msg_id = self._msg_ids.pop(0)
            if self._received_timeout and self._dpa_timeout is not None:
                self._received_timeout = False
                raise DpaRequestTimeoutError(f'DPA request timed out (timeout {self._dpa_timeout} seconds).')
            else:
                if self._received_timeout:
                    self._received_timeout = False
                    raise JsonRequestTimeoutError(
                        f'Response message to request with ID {msg_id} received, but DPA request timed out.'
                    )
                elif self._unsupported:
                    self._unsupported = False
                    raise JsonResponseNotSupportedError(
                        f'Response message to request with ID {msg_id} received, but is not supported.'
                    )
                else:
                    raise JsonRequestTimeoutError(
                        f'Response message to request with ID {msg_id} not received within the specified time of '
                        f'{timeout_to_use} seconds.')
        return self._response

    def send_and_receive(self, request: IRequest, timeout: Optional[float] = None) -> Optional[IResponse]:
        """Publish request to request topic and wait for response.

        If request nadr is :obj:`IQMESH_TEMP_ADDR` (254) or :obj:`BROADCAST_ADDR` (255),
        the method does not wait for a response message and returns :obj:`None`.

        Args:
            request (IRequest): Request to publish.
            timeout (float, optional): Time to wait for request to be processed and response sent.
                If not specified, :obj:`global_request_timeout` is used.
        """
        self.send(request)
        if request.nadr in [IQMESH_TEMP_ADDR, BROADCAST_ADDR]:
            return None
        return self.receive(timeout)

    def set_receive_callback(self, callback: Callable[[IResponse], None]) -> None:
        """Assign callback for messages published to the response topic.

        Args:
            callback (Callable[[IResponse], None]): Callback used to process messages published to response topic.
        """
        self._callback = callback
