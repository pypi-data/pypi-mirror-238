## Changelog

### Version: 0.1.48

Release date: 31.10.2023

#### Changes

- OS TR configuration data now stores reserved data blocks

### Version: 0.1.47

Release date: 31.10.2023

#### Changes

- Fixed OS `BatchRequest` and `SelectiveBatchRequest` data length validation
- Fixed OS TR configuration data embedded peripherals parsing

### Version: 0.1.46

Release date: 17.10.2023

#### Changes

- Added getter methods for `OsTrConfData` members
- Fixed RAM `WriteRequest` data length validation

### Version: 0.1.45

Release date: 13.10.2023

#### Changes

- Added OS Batch, SelectiveBatch, Indicate and WriteTrConfByte messages and response factories
- Added generic serialization and deserialization methods for requests and responses
- Deduplicated serialization and deserialization code of messages
- Removed unused imports

### Version: 0.1.44

Release date: 29.08.2023

#### Changes

- Fixed `GenericResponse` parsing method `from_dpa`

### Version: 0.1.43

Release date: 29.08.2023

#### Changes

- Allow user peripheral numbers to be used in messages

### Version: 0.1.42

Release date: 28.08.2023

#### Changes

- `MqttTransport` method `send_and_receive` now returns `None` if request
  address is `IQMESH_TEMP_ADDR`(254) or `BROADCAST_ADDR`(255).

### Version: 0.1.41

Release date: 25.08.2023

#### Changes

- Added parameter to response factory from dpa to allow use of GenericResponse in case of unknown peripheral 
  number or peripheral command.

### Version: 0.1.40

Release date: 25.08.2023

#### Changes

- Added docstrings across the library
- Added Binary Output standard messages and response factories
- Added a `GenericRequest` and `GenericResponse` messages
- Added IO constants to `dpa` utility module
- Updated return types across the library
- Changed response messages' data return types to `Optional` for situations where request was not handled successfully
- Fixed some codestyle, doc style and linter errors
- Removed some unused auxiliary methods

### Version: 0.1.39

Release date: 07.08.2023

#### Changes

- Reworked factory methods
- Updated typeguard dependency

### Version: 0.1.38

Release date: 07.08.2023

#### Changes

- Fixed typeguard version to 4.0.0

### Version: 0.1.37

Release date: 01.08.2023

#### Changes

- Added `FrcCommands` enum to DPA utils
- Added `FrcParser` class
- Updated `SensorFrcErrors` enum to use strings and added factory method from integer values

### Version: 0.1.36

Release date: 31.07.2023

#### Changes

- Fixed FRC commands of `TemperatureFloat` and `Length` quantities

### Version: 0.1.35

Release date: 31.07.2023

#### Changes

- Changed `Power` quantity short name
- Added `TemperatureFloat` and `Length` quantities
- Fixed data block parsing data in `SensorParser`
- Fixed FRC data conversion errors

### Version: 0.1.34

Release date: 30.07.2023

#### Changes

- Removed unused Sensor FRC request
- Added missing 2bit FRC command to `BinaryData7` quantity

### Version: 0.1.33

Release date: 20.07.2023

#### Changes

- Added missing quantities to `SensorParser` method `frc_convert`
- Fixed data block parsing in `SensorParser`
- Removed trailing comma in `TimeSpan` quantity definition
- Fixed `short_name` member in `ShortLength` quantity definition

### Version: 0.1.32

Release date: 19.07.2023

#### Changes

- Fixed a bug where `PeripheralEnumeration` response data was parsed by `PeripheralInformation` response factory
- Added `coordinator_shift` parameter to `bitmap_to_nodes` method to ignore first bit
- Updated `BondedDevices` and `DiscoveredDevices` responses to parse only first 30 bytes of PDATA

### Version: 0.1.31

Release date: 10.07.2023

#### Changes

- Fixed a bug where EEEPROM responses were handled by EEPROM response factories

### Version: 0.1.30

Release date: 01.07.2023

#### Changes

- Updated `Temperature` quantity short name from `t` to `T`
- Added EEEPROM, RAM and IO peripherals
- Added missing submodule imports
- Fixed validation of EEPROM `WriteRequest` data length

### Version: 0.1.29

Release date: 28.06.2023

#### Changes

- Fixed conversion of temperature measurement from 1B FRC data in `SensorParser`
- Removed a debug print from Thermometer `Read` response

### Version: 0.1.28

Release date: 27.06.2023

#### Changes

- Fixed return type hint of Sensor `ReadSensors` response factory methods
- Added missing type hint to `ResponseCodes` method `to_string`
- Separated quantity data from `sensor_parser` module into `quantity_data` module
- Sensor parsing methods now raise `UnknownSensorTypeError` instead of `ValueError`
- Updated docstrings for utils submodule

### Version: 0.1.27

Release date: 24.06.2023

#### Changes

- Added validation of `dpa_rsp_time` and `dev_process_time` IRequest properties
- Fixed Sensor FRC error codes handling
- Fixed trimming of `frc_data` in `frc_dpa` method of `SensorParser`, the method now assumes `frc_data` does not include status byte
- Fixed 2B FRC data conversion in `SensorParser`
- Reworked data trimming by FRC data size in `SensorParser`
- Added parsing of 2b FRC responses to `SensorParser`

### Version: 0.1.26

Release date: 22.06.2023

#### Changes

- Added `dev_process_time` parameter to request classes
- Changed `timeout` parameter of request classes to `dpa_rsp_time`
- Added Sensor `ReadSensors` request (without types)
- Added parsing method for `ReadSensors` response and FRC responses
- Updated typeguard dependency version
- `ResponseCodes` method `to_string` now includes flags

### Version: 0.1.25

Release date: 18.06.2023

#### Changes

- Added FRC peripheral requests, responses, response factories and DPA constants
- Added Sensor Enumerate and Read requests, responses, response factories
- Added Sensor parser and types
- Fixed incorrect OS `WRITE_CFG` response command value
- Refactored OS `ReadTrConfResponse` and `WriteTrConfRequest` data into a single class, added serialization and deserialization methods
- Replaced regular getter and setter methods with `@property` decorators (`response.get_rcode()` -> `response.rcode`)
- Updated Exploration `PeripheralInformationResponse` and `MorePeripheralsInformationResponse` classes to work with basic JSON API response data instead of results for the purposes of matching DPA and JSON API responses

### Version: 0.1.24

Release date: 31.05.2023

#### Changes

- Added Node peripheral commands
- Added OS peripheral commands reset, restore,
- Added new Node and OS peripheral imports to `messages`
- Added new Node and OS peripheral response factories
- Changed `UartOpenRequest` to accept baud rate parameter as both `BaudRates` enum member and integer
- Changed `OsReadData` parameter from `result` to `data`
- Removed unnecessary result fetching in `from_json` factory method of `ClearAllBondsResponse`
- Fixed parameter types of `AsyncResponse`
- Updated error message in `response_length` DPA validator
- MqttTransport now does not wait for responses to broadcast messages
- Added more constants to `dpa` utils

### Version: 0.1.23

Release date: 25.05.2023

#### Changes

- Updated `ResponseCodes` method `to_string` messages.
- Moved UART baud rate enum from UART Open request to `dpa` submodule.

### Version: 0.1.22

Release date: 23.05.2023

#### Changes

- Fixed rcode value comparison condition in `ResponseCodes` method `to_string`

### Version: 0.1.21

Release date: 22.05.2023

#### Changes

- Added check for values out of range to `ResponseCodes` method `to_string`
- Fixed missing return statements

### Version: 0.1.20

Release date: 20.05.2023

#### Changes

- Added missing DPA error constants to `ResponseCodes`
- Added string representation of `ResponseCodes` values and `to_string` classmethod
- Used ResponseCodes constants throughout the library where unused

### Version: 0.1.19

Release date: 17.05.2023

#### Changes

- Added Device Exploration (unfinished due to pending changes in IQRF Gateway Daemon), UART and Thermometer peripheral request, responses and response factories
- Added `terminate` method to `MqttTransport` to disconnect client and stop event loop peacefully
- MQTT transport initialization now waits for subscription confirmation instead of connection confirmation

### Version: 0.1.18

Release date: 10.05.2023

#### Changes

- Added `is_connected` method to `MqttTransport`
- Fixed matching of sent requests and received responses in MQTT transport
- MQTT transport now distinguishes DPA request timeout without user-specified timeout, DPA request timeout with user-specified timeout, JSON request timeout

### Version: 0.1.17

Release date: 09.05.2023

#### Changes

- Fixed validation of `IRequest` parameter `nadr`

### Version: 0.1.16

Release date: 03.05.2023

#### Changes

- Added setters for EEPROM requests
- Fixed generation of random UUID message ID for requests
- Separated DPA and JSON timeout in MQTT transport
- Added optional timeout parameter to requests

### Version: 0.1.15

Release date: 02.05.2023

#### Changes

- Fixed `peripherals` module submodule imports

### Version: 0.1.14

Release date: 27.04.2023

#### Changes

- Changed module tree structure
  - `iqrfpy.messages.requests.<peripheral>` -> `iqrfpy.peripherals.<peripheral>.requests`
  - `iqrfpy.messages.responses.<peripheral>` -> `iqrfpy.peripherals.<peripheral>.responses`
- Moved `async_response`, `confirmation`, `irequest`, `iresponse` and `response_factory` submodules to `iqrfpy` module
- Renamed `peripheral_messages` submodule to `messages`
- Added specific peripheral submodule imports to `periphral` submodule
- Added missing submodule imports
- Added `send_and_receive` method overloads for individual requests and responses to `MqttTransport`

### Version: 0.1.13

Release date: 26.04.2023

#### Changes

- Added EEPROM peripheral requests, responses and response factories
- Added EEPROM peripheral to `Common` class auxiliary methods
- Changed `response_factory` Coordinator response imports to named namespace import
- Added `iqrfpy.peripheral_messages` module containing imports and wildcard import for all available requests and responses
- Simplified validation of request parameters, deferring much of the work to the DPA layer

### Version: 0.1.12

Release date: 24.04.2023

#### Changes

- Added LEDG peripheral requests, responses and response factories
- Fixed undefined variable warning when selecting a response factory
- Added wildcard imports to `iqrfpy.exceptions` module
- Added `iqrfpy.utils.validators` module containing validator classes for DPA and JSON responses
- Updated validation of DPA and JSON responses in factory methods
- Added optional timeout parameter to `receive` method of `MqttTransport`
- `MqttTransport` onmessage callback now checks if received JSON API response indicates DPA request timeout

### Version: 0.1.11

Release date: 20.04.2023

#### Changes

- Added `LOCAL_DEVICE_ADDR` and `BROADCAST_ADDR` constants to `iqrfpy.utils.dpa` module
- Added `list_to_hex_string` auxiliary method to `Common` class
- Changed `IRequest` validation of `nadr` to include local device, temporary iqmesh and broadcast addresses
- Added `OsReadFlags` and `OsReadSlotLimits` dataclasses
- Added response data getters to OS `ReadResponse`

### Version: 0.1.10

Release date: 20.04.2023

#### Changes

- Added missing wildcard imports to `response_factory` module
- Removed `synchronous` parameter from `MqttTransport`
- `MqttTransport` now passes received message to user-specified callback regardless of communication mode
- Implemented method `send_and_receive` of `MqttTransport`

### Version: 0.1.9

Release date: 20.04.2023

#### Changes

- Added OS `ReadResponse` response factory
- Added synchronous MQTT transport communication
- Added `TransportNotConnectedError` and `MessageNotReceivedError` exceptions

### Version: 0.1.8

Release date: 19.04.2023

#### Changes

- Unified class file name and class name cases
- Moved validation of `AuthorizeBondRequest` parameters to `AuthorizeBondParams` class
- Added validation of `AuthorizeBondParams` count to `AuthorizeBondRequest`
- Added LEDR peripheral requests, responses and response factories
- Added OS peripheral Read request and response
- Added exceptions for unsupported peripherals and peripheral commands
- `ResponseFactory` methods now throw relevant exceptions when an unknown or unsupported peripheral or peripheral command is processed
- Added method `send_and_receive` to `ITransport`
- Added abstract method decorators to `ITransport` methods
- Added `MqttTransportParams` dataclass and removed individual parameters from `MqttTransport` constructor
- Added asynchronous MQTT transport communication
- Added docstrings for enums

### Version: 0.1.7

Release date: 17.04.2023

#### Changes

- Added `receive` and `confirmation` methods to `ITransport`

### Version: 0.1.6

Release date: 15.04.2023

#### Changes

- Added module `iqrfpy.utils.dpa` containing DPA constants
- Replaced magical constants throughout the source code with named DPA constants
- Exposed request and response submodules imports

### Version: 0.1.5

Release date: 07.04.2023

#### Changes

- Added module `iqrfpy.exceptions` containing custom exceptions
- Replaced generic Error types with custom exceptions

### Version: 0.1.4

Release date: 06.04.2023

#### Changes

- `ITransport` methods now raise `NotImplementedError`
- Added `set_receive_callback` method to `ITransport`
- Removed `receive` and `receive_async` methods from `ITransport`

### Version: 0.1.3

Release date: 02.04.2023

#### Changes

- Added `AuthorizeBondParams` dataclass for `AuthorizeBondRequest`
- Added validation of `AuthorizeBondRequest` parameters
- Added response factory for `AuthorizeBondResponse`

### Version: 0.1.2

Release date: 27.03.2023

#### Changes

- Added wildcard imports for response factories

### Version: 0.1.1 (unreleased)

Release date: N/A

#### Changes

- Unified module name cases
- Added typechecking for classes
- Added enum class `IntEnumMember` with `has_value` method
- Changed existing integer enums to extend `IntEnumMember`
- Added response factories to parse DPA and JSON responses into response objects
- Renamed `data` parameter to `dpa` in DPA response factory methods
- Renamed `data` parameter to `json` in JSON response factory methods
- Moved `IRequest` class to `requests` module
- Moved `AsyncResponse`, `Confirmation` and `IResponse` class to `responses` module
- Added more auxiliary methods to `Common` class

### Version: 0.1.0 (unreleased)

Release date: N/A

#### Changes

- Basic project structure
- Added peripheral enums
- Added peripheral request and response command enums
- Added message type enums
- Added class Common providing auxiliary functions
- Added abstract classes for requests, responses and transports
- Added asynchronous responses
- Added confirmation message
- Added Coordinator peripheral requests and responses
- Added MQTT transport
- Added simple tests for Coordinator peripheral, enums and Common class
