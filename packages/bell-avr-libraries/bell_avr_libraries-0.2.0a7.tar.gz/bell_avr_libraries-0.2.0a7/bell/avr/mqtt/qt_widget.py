# This file is automatically @generated. DO NOT EDIT!
# fmt: off

from __future__ import annotations

from typing import Literal, Optional, Union, overload

import pydantic
from PySide6 import QtCore, QtWidgets

from bell.avr.mqtt.constants import _MQTTTopicCallableTypedDict
from bell.avr.mqtt.serializer import deserialize_payload, serialize_payload
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


class MQTTWidget(QtWidgets.QWidget):
    send_message_signal: QtCore.SignalInstance = QtCore.Signal(str, bytes)  # type: ignore
    """
    This should not be used directly, but rather through `send_message` instead.

    This is a `QtCore.Signal` that expects a topic, and the str/bytes of the
    MQTT payload. This should already be serialized with
    `bell.avr.mqtt.serializer.serialize_payload` and ready for transmission over the
    network.
    """

    def __init__(self, parent: Optional[QtWidgets.QWidget]) -> None:
        """
        This class is desgined for Qt applications where a widget needs to receive and
        send MQTT messages. After the widget is initialized, the signals need to be
        connected.

        Example:

        ```python
        from bell.avr.mqtt.qt_widget import MQTTWidget


        class ThermalViewControlWidget(MQTTWidget):
            ...


        thermal_view_control_widget = ThermalViewControlWidget()

        # connect the `on_message` function to incoming messages
        main_connection_widget.mqtt_connection_widget.mqtt_client.on_message_signal.connect(
            thermal_view_control_widget.on_message
        )

        # connect the `send_message_signal` signal to the mqtt client to send messages
        thermal_view_control_widget.send_message_signal.connect(
            main_connection_widget.mqtt_connection_widget.mqtt_client._publish
        )
        ```
        """
        # this docstring is here because of pdoc weirdness

        self.topic_callbacks: _MQTTTopicCallableTypedDict = {}
        """
        See `bell.avr.mqtt.client.MQTTClient.topic_callbacks`.
        """

        super().__init__(parent)


    @overload
    def send_message(self, topic: Literal["avr/pcm/color/set"], payload: Union[AVRPCMColorSet, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/pcm/color/timed"], payload: Union[AVRPCMColorTimed, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/pcm/laser/fire"], payload: Union[AVREmptyMessage, dict, None] = None) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/pcm/laser/on"], payload: Union[AVREmptyMessage, dict, None] = None) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/pcm/laser/off"], payload: Union[AVREmptyMessage, dict, None] = None) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/pcm/servo/open"], payload: Union[AVRPCMServo, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/pcm/servo/close"], payload: Union[AVRPCMServo, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/pcm/servo/pwm/min"], payload: Union[AVRPCMServoPWM, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/pcm/servo/pwm/max"], payload: Union[AVRPCMServoPWM, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/pcm/servo/percent"], payload: Union[AVRPCMServoPercent, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/pcm/servo/absolute"], payload: Union[AVRPCMServoAbsolute, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/action/capture_home"], payload: Union[AVREmptyMessage, dict, None] = None) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/action/sleep"], payload: Union[AVRFCMActionSleep, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/action/arm"], payload: Union[AVREmptyMessage, dict, None] = None) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/action/disarm"], payload: Union[AVREmptyMessage, dict, None] = None) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/action/kill"], payload: Union[AVREmptyMessage, dict, None] = None) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/action/land"], payload: Union[AVREmptyMessage, dict, None] = None) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/action/takeoff"], payload: Union[AVRFCMActionTakeoff, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/action/reboot"], payload: Union[AVREmptyMessage, dict, None] = None) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/action/goto/global"], payload: Union[AVRFCMGoToGlobal, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/action/goto/local"], payload: Union[AVRFCMGoToLocal, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/action/mission/upload"], payload: Union[AVRFCMMissionUpload, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/action/mission/start"], payload: Union[AVREmptyMessage, dict, None] = None) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/hil_gps/stats"], payload: Union[AVRFCMHILGPSStats, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/airborne"], payload: Union[AVRFCMAirborne, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/landed"], payload: Union[AVRFCMLanded, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/battery"], payload: Union[AVRFCMBattery, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/armed"], payload: Union[AVRFCMArmed, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/flight_mode"], payload: Union[AVRFCMFlightMode, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/position/local"], payload: Union[AVRFCMPositionLocal, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/position/global"], payload: Union[AVRFCMPositionGlobal, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/position/home"], payload: Union[AVRFCMPositionHome, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/attitude/euler/degrees"], payload: Union[AVRFCMAttitudeEulerDegrees, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/velocity"], payload: Union[AVRFCMVelocity, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fcm/gps/info"], payload: Union[AVRFCMGPSInfo, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fusion/position/local"], payload: Union[AVRFusionPositionLocal, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fusion/velocity"], payload: Union[AVRFusionVelocity, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fusion/position/global"], payload: Union[AVRFusionPositionGlobal, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fusion/groundspeed"], payload: Union[AVRFusionGroundspeed, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fusion/course"], payload: Union[AVRFusionCourse, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fusion/heading"], payload: Union[AVRFusionHeading, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fusion/climb_rate"], payload: Union[AVRFusionClimbRate, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fusion/attitude/quaternion"], payload: Union[AVRFusionAttitudeQuaternion, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fusion/attitude/euler/radians"], payload: Union[AVRFusionAttitudeEulerRadians, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/fusion/hil_gps/message"], payload: Union[AVRFusionHILGPSMessage, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/vio/resync"], payload: Union[AVRVIOResync, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/vio/position/local"], payload: Union[AVRVIOPositionLocal, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/vio/velocity"], payload: Union[AVRVIOVelocity, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/vio/attitude/euler/radians"], payload: Union[AVRVIOAttitudeEulerRadians, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/vio/attitude/quaternion"], payload: Union[AVRVIOAttitudeQuaternion, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/vio/heading"], payload: Union[AVRVIOHeading, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/vio/confidence"], payload: Union[AVRVIOConfidence, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/vio/image/capture"], payload: Union[AVRVIOImageCapture, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/vio/image/request"], payload: Union[AVRVIOImageRequest, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/vio/image/stream/enable"], payload: Union[AVRVIOImageStreamEnable, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/vio/image/stream/disable"], payload: Union[AVREmptyMessage, dict, None] = None) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/apriltags/vehicle_position"], payload: Union[AVRAprilTagsVehiclePosition, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/apriltags/raw"], payload: Union[AVRAprilTagsRaw, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/apriltags/visible"], payload: Union[AVRAprilTagsVisible, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/apriltags/status"], payload: Union[AVRAprilTagsStatus, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/status/led/pcm"], payload: Union[AVREmptyMessage, dict, None] = None) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/status/led/vio"], payload: Union[AVREmptyMessage, dict, None] = None) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/status/led/apriltags"], payload: Union[AVREmptyMessage, dict, None] = None) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/status/led/fcm"], payload: Union[AVREmptyMessage, dict, None] = None) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/status/led/thermal"], payload: Union[AVREmptyMessage, dict, None] = None) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/thermal/reading"], payload: Union[AVRThermalReading, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/autonomous/enable"], payload: Union[AVREmptyMessage, dict, None] = None) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/autonomous/disable"], payload: Union[AVREmptyMessage, dict, None] = None) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/autonomous/building/enable"], payload: Union[AVRAutonomousBuildingEnable, dict]) -> None: ...
    @overload
    def send_message(self, topic: Literal["avr/autonomous/building/disable"], payload: Union[AVRAutonomousBuildingDisable, dict]) -> None: ...

    def send_message(self, topic: str, payload: Union[pydantic.BaseModel, dict, None] = None) -> None:
        """
        Send a message on a topic with a given payload. The payload can be
        a Python class or  aPython dictionary, much like
        `bell.avr.mqtt.module.MQTTModule.send_message`.

        For this application, this emits a Qt Signal for a message to be sent to the
        MQTT client.
        """
        raw_payload = serialize_payload(topic, payload)
        self.send_message_signal.emit(topic, raw_payload)

    def on_message(self, topic: str, payload: bytes) -> None:
        """
        Process messages received from the MQTT client. The `payload` argument
        is the *raw* payload data that has not been deserialzed yet.
        """
        klass_payload = deserialize_payload(topic, payload)
        dispatch_message(self.topic_callbacks, topic, klass_payload)