# This file is automatically @generated. DO NOT EDIT!
# fmt: off

from __future__ import annotations
import copy
from typing import Any, Literal, Union, overload

import paho.mqtt.client as paho_mqtt
import pydantic
from loguru import logger

from bell.avr.mqtt.client import MQTTClient
from bell.avr.mqtt.constants import _MQTTTopicPayloadTypedDict
from bell.avr.mqtt.dispatcher import dispatch_message
from bell.avr.mqtt.payloads import (
    AVRPCMColorSet,
    AVRPCMColorTimed,
    AVREmptyMessage,
    AVRPCMServo,
    AVRPCMServoPWM,
    AVRPCMServoPercent,
    AVRPCMServoAbsolute,
    AVRFCMActionSleep,
    AVRFCMActionTakeoff,
    AVRFCMGoToGlobal,
    AVRFCMGoToLocal,
    AVRFCMMissionUpload,
    AVRFCMHILGPSStats,
    AVRFCMAirborne,
    AVRFCMLanded,
    AVRFCMBattery,
    AVRFCMArmed,
    AVRFCMFlightMode,
    AVRFCMPositionLocal,
    AVRFCMPositionGlobal,
    AVRFCMPositionHome,
    AVRFCMAttitudeEulerDegrees,
    AVRFCMVelocity,
    AVRFCMGPSInfo,
    AVRFusionPositionLocal,
    AVRFusionVelocity,
    AVRFusionPositionGlobal,
    AVRFusionGroundspeed,
    AVRFusionCourse,
    AVRFusionHeading,
    AVRFusionClimbRate,
    AVRFusionAttitudeQuaternion,
    AVRFusionAttitudeEulerRadians,
    AVRFusionHILGPSMessage,
    AVRVIOResync,
    AVRVIOPositionLocal,
    AVRVIOVelocity,
    AVRVIOAttitudeEulerRadians,
    AVRVIOAttitudeQuaternion,
    AVRVIOHeading,
    AVRVIOConfidence,
    AVRVIOImageCapture,
    AVRVIOImageRequest,
    AVRVIOImageStreamEnable,
    AVRAprilTagsVehiclePosition,
    AVRAprilTagsRaw,
    AVRAprilTagsVisible,
    AVRAprilTagsStatus,
    AVRThermalReading,
    AVRAutonomousBuildingEnable,
    AVRAutonomousBuildingDisable,
)
from bell.avr.mqtt.serializer import deserialize_payload, serialize_payload


class MQTTModule(MQTTClient):
    """
    This is a boilerplate module for AVR that makes it very easy to send
    and receive MQTT messages and do something with them.

    Here is an example of a module that changes the LED color every 5 seconds:
    ```python
    import random
    import time

    from bell.avr.mqtt.module import MQTTModule
    from bell.avr.mqtt.payloads import AVRPCMColorSet


    class Sandbox(MQTTModule):
        def update_led(self) -> None:
            wrgb = tuple(random.randint(0, 255) for _ in range(4))
            self.send_message("avr/pcm/color/set", AVRPCMColorSet(wrgb=wrgb))

        def run(self) -> None:
            super().run_non_blocking()

            while True:
                time.sleep(5)
                self.update_led()


    if __name__ == "__main__":
        box = Sandbox()
        box.run()
    ```

    For a fully commented code example, see
    [AVR-VMC-Sandbox-Module](https://github.com/bellflight/AVR-VMC-Sandbox-Module).

    See `bell.avr.mqtt.client.MQTTClient.topic_callbacks` for more information on how to set up callbacks.

    Additionally, the `message_cache` attribute is a dictionary that holds
    a copy of the last payload sent by that module on a given topic. The keys are the
    topic strings, and the values are the topic payloads.
    """
    def __init__(self):
        super().__init__()

        self.message_cache: _MQTTTopicPayloadTypedDict = {}
        """
        The `message_cache` attribute is a dictionary that holds
        a copy of the last payload sent by *that* module on a given topic.
        The keys are the topic strings, and the values are the topic payloads.
        This can be useful for doing operations based on the last known state
        of a topic.

        Example from the Fusion module:

        ```python
        if "avr/fusion/heading" in self.message_cache:
            heading = int(self.message_cache["avr/fusion/heading"].hdg * 100)
        else:
            logger.debug("Waiting for avr/fusion/attitude/heading to be populated")
            return
        ```
        """

    def on_message(self, client: paho_mqtt.Client, userdata: Any, msg: paho_mqtt.MQTTMessage) -> None:
        """
        Process and dispatch an incoming message. This is called automatically.
        """
        payload = deserialize_payload(msg.topic, msg.payload)

        if self.enable_verbose_logging:
            logger.debug(f"Recieved {msg.topic}: {msg.payload}")

        dispatch_message(self.topic_callbacks, msg.topic, payload)

    @overload
    def send_message(self, topic: Literal["avr/pcm/color/set"], payload: Union[AVRPCMColorSet, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/pcm/color/timed"], payload: Union[AVRPCMColorTimed, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/pcm/laser/fire"], payload: Union[AVREmptyMessage, dict, None] = None, force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/pcm/laser/on"], payload: Union[AVREmptyMessage, dict, None] = None, force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/pcm/laser/off"], payload: Union[AVREmptyMessage, dict, None] = None, force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/pcm/servo/open"], payload: Union[AVRPCMServo, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/pcm/servo/close"], payload: Union[AVRPCMServo, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/pcm/servo/pwm/min"], payload: Union[AVRPCMServoPWM, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/pcm/servo/pwm/max"], payload: Union[AVRPCMServoPWM, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/pcm/servo/percent"], payload: Union[AVRPCMServoPercent, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/pcm/servo/absolute"], payload: Union[AVRPCMServoAbsolute, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/action/capture_home"], payload: Union[AVREmptyMessage, dict, None] = None, force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/action/sleep"], payload: Union[AVRFCMActionSleep, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/action/arm"], payload: Union[AVREmptyMessage, dict, None] = None, force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/action/disarm"], payload: Union[AVREmptyMessage, dict, None] = None, force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/action/kill"], payload: Union[AVREmptyMessage, dict, None] = None, force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/action/land"], payload: Union[AVREmptyMessage, dict, None] = None, force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/action/takeoff"], payload: Union[AVRFCMActionTakeoff, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/action/reboot"], payload: Union[AVREmptyMessage, dict, None] = None, force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/action/goto/global"], payload: Union[AVRFCMGoToGlobal, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/action/goto/local"], payload: Union[AVRFCMGoToLocal, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/action/mission/upload"], payload: Union[AVRFCMMissionUpload, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/action/mission/start"], payload: Union[AVREmptyMessage, dict, None] = None, force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/hil_gps/stats"], payload: Union[AVRFCMHILGPSStats, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/airborne"], payload: Union[AVRFCMAirborne, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/landed"], payload: Union[AVRFCMLanded, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/battery"], payload: Union[AVRFCMBattery, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/armed"], payload: Union[AVRFCMArmed, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/flight_mode"], payload: Union[AVRFCMFlightMode, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/position/local"], payload: Union[AVRFCMPositionLocal, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/position/global"], payload: Union[AVRFCMPositionGlobal, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/position/home"], payload: Union[AVRFCMPositionHome, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/attitude/euler/degrees"], payload: Union[AVRFCMAttitudeEulerDegrees, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/velocity"], payload: Union[AVRFCMVelocity, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/gps/info"], payload: Union[AVRFCMGPSInfo, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fusion/position/local"], payload: Union[AVRFusionPositionLocal, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fusion/velocity"], payload: Union[AVRFusionVelocity, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fusion/position/global"], payload: Union[AVRFusionPositionGlobal, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fusion/groundspeed"], payload: Union[AVRFusionGroundspeed, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fusion/course"], payload: Union[AVRFusionCourse, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fusion/heading"], payload: Union[AVRFusionHeading, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fusion/climb_rate"], payload: Union[AVRFusionClimbRate, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fusion/attitude/quaternion"], payload: Union[AVRFusionAttitudeQuaternion, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fusion/attitude/euler/radians"], payload: Union[AVRFusionAttitudeEulerRadians, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fusion/hil_gps/message"], payload: Union[AVRFusionHILGPSMessage, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/vio/resync"], payload: Union[AVRVIOResync, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/vio/position/local"], payload: Union[AVRVIOPositionLocal, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/vio/velocity"], payload: Union[AVRVIOVelocity, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/vio/attitude/euler/radians"], payload: Union[AVRVIOAttitudeEulerRadians, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/vio/attitude/quaternion"], payload: Union[AVRVIOAttitudeQuaternion, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/vio/heading"], payload: Union[AVRVIOHeading, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/vio/confidence"], payload: Union[AVRVIOConfidence, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/vio/image/capture"], payload: Union[AVRVIOImageCapture, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/vio/image/request"], payload: Union[AVRVIOImageRequest, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/vio/image/stream/enable"], payload: Union[AVRVIOImageStreamEnable, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/vio/image/stream/disable"], payload: Union[AVREmptyMessage, dict, None] = None, force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/apriltags/vehicle_position"], payload: Union[AVRAprilTagsVehiclePosition, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/apriltags/raw"], payload: Union[AVRAprilTagsRaw, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/apriltags/visible"], payload: Union[AVRAprilTagsVisible, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/apriltags/status"], payload: Union[AVRAprilTagsStatus, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/status/led/pcm"], payload: Union[AVREmptyMessage, dict, None] = None, force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/status/led/vio"], payload: Union[AVREmptyMessage, dict, None] = None, force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/status/led/apriltags"], payload: Union[AVREmptyMessage, dict, None] = None, force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/status/led/fcm"], payload: Union[AVREmptyMessage, dict, None] = None, force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/status/led/thermal"], payload: Union[AVREmptyMessage, dict, None] = None, force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/thermal/reading"], payload: Union[AVRThermalReading, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/autonomous/enable"], payload: Union[AVREmptyMessage, dict, None] = None, force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/autonomous/disable"], payload: Union[AVREmptyMessage, dict, None] = None, force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/autonomous/building/enable"], payload: Union[AVRAutonomousBuildingEnable, dict], force_write: bool = False) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/autonomous/building/disable"], payload: Union[AVRAutonomousBuildingDisable, dict], force_write: bool = False) -> None: ...

    def send_message(self, topic: str, payload: Union[pydantic.BaseModel, dict, None] = None, force_write: bool = False) -> None:
        """
        Sends a message to the MQTT broker. This expects a topic to send the message
        on, and the payload for the message. The payload can either be a class
        or a dictionary.

        Example:

        ```python
        from bell.avr.mqtt.payloads import AVRPCMServoAbsolute

        ...

        # Python class
        self.send_message("avr/pcm/servo/absolute", AVRPCMServoAbsolute(servo=2, position=100))

        # Python dicts
        self.send_message("avr/pcm/servo/absolute", {"servo": 2, "position": 100})
        ```

        Using Python classes are highly recommended as this performs
        extra validation checks.

        For `send_message` to work, either `run` or `run_non_blocking` must have
        already been called.

        Enabling `force_write` will
        forcefully send the message, bypassing threading mutex. Only use this
        if you know what you're doing.
        """
        str_payload = serialize_payload(topic, payload)
        self._publish(topic, str_payload, force_write)
        self.message_cache[topic] = copy.deepcopy(payload)