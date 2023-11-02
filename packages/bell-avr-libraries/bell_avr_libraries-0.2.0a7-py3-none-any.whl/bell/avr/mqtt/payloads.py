# This file is automatically @generated. DO NOT EDIT!
# fmt: off

"""
These are Python classes for MQTT message payloads.
As AVR exclusively uses JSON, these are all [Pydantic](https://docs.pydantic.dev/)
classes that have all of the required fields for a message.

This is a Python implementation of the AVR [AsyncAPI definition](../mqtt/asyncapi).

Example:

```python
from bell.avr.mqtt.payloads import AVRPCMColorSet

payload = AVRPCMColorSet(wrgb=(128, 232, 142, 0))```
Some of the Python documentation does not get generated correctly,
please refer to the above AsyncAPI definition, or the "View Source" dropdowns
on the right side.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Literal, Optional, Protocol, Tuple, Type, Union, overload

from pydantic import BaseModel as PydanticBaseModel
from pydantic import RootModel as PydanticRootModel
from pydantic import ConfigDict, Field, conlist, field_validator


@overload
def _convert_type(iter_in: Union[list, tuple], iter_out: Type[list], items_convert_to: Type[int]) -> List[int]: ...

@overload
def _convert_type(iter_in: Union[list, tuple], iter_out: Type[list], items_convert_to: Type[float]) -> List[float]: ...

@overload
def _convert_type(iter_in: Union[list, tuple], iter_out: Type[tuple], items_convert_to: Type[int]) -> Tuple[int, ...]: ...

@overload
def _convert_type(iter_in: Union[list, tuple], iter_out: Type[tuple], items_convert_to: Type[float]) -> Tuple[float, ...]: ...

def _convert_type(iter_in: Union[list, tuple], iter_out: Union[Type[list], Type[tuple]], items_convert_to: Union[Type[int], Type[float]]) -> Union[tuple, list, int, float]:
    if isinstance(iter_in, (tuple, list)):
        return iter_out(_convert_type(x, iter_out, items_convert_to) for x in iter_in)
    else:
        return items_convert_to(iter_in)


class BaseModel(PydanticBaseModel):
    'For [Pydantic configuration](https://docs.pydantic.dev/latest/usage/model_config/), please ignore.'
    model_config = ConfigDict(extra="forbid")

class AVREmptyMessage(BaseModel):
    """
    This is an empty class to be used with topics with no payload. When data is sent on a topic that expects `AVREmptyMessage`, an empty string, or an empty dict (`{}`) are both acceptable.
    """

    pass

class AVRPCMColorSetWrgbItem(PydanticRootModel):
    root: int = Field(..., ge=0, le=255)

    def __int__(self) -> int:
        return self.root


class AVRPCMColorSet(BaseModel):
    if TYPE_CHECKING:
        wrgb: Tuple[int, int, int, int]
    else:
        wrgb: conlist(AVRPCMColorSetWrgbItem, min_length=4, max_length=4)
    """
    Color values for the white, red, green, and blue channels, respectively.
    """
    @field_validator('wrgb')
    def _validate_wrgb(cls, v) -> tuple: # pyright: ignore
        # Function to convert list of objects into simpler types
        return _convert_type(v, tuple, int)


class AVRPCMColorTimedWrgbItem(PydanticRootModel):
    root: int = Field(..., ge=0, le=255)

    def __int__(self) -> int:
        return self.root


class AVRPCMColorTimed(BaseModel):
    if TYPE_CHECKING:
        wrgb: Tuple[int, int, int, int]
    else:
        wrgb: conlist(AVRPCMColorTimedWrgbItem, min_length=4, max_length=4)
    """
    Color values for the white, red, green, and blue channels, respectively.
    """
    @field_validator('wrgb')
    def _validate_wrgb(cls, v) -> tuple: # pyright: ignore
        # Function to convert list of objects into simpler types
        return _convert_type(v, tuple, int)

    time: float = Field(default=0.5, ge=0)
    """
    Number of seconds the color should be set for. Default is 0.5.
    """

class AVRPCMServo(BaseModel):
    servo: int = Field(..., ge=0, le=15)
    """
    Servo ID. This is 0-indexed.
    """

class AVRPCMServoPWM(BaseModel):
    servo: int = Field(..., ge=0, le=15)
    """
    Servo ID. This is 0-indexed.
    """
    pulse: int = Field(..., ge=0, le=1000)
    """
    Pulse width.
    """

class AVRPCMServoPercent(BaseModel):
    servo: int = Field(..., ge=0, le=15)
    """
    Servo ID. This is 0-indexed.
    """
    percent: int = Field(..., ge=0, le=100)
    """
    Servo percent. 0 is closed, and 100 is open.
    """

class AVRPCMServoAbsolute(BaseModel):
    servo: int = Field(..., ge=0, le=15)
    """
    Servo ID. This is 0-indexed.
    """
    position: int
    """
    Absolute position of the servo.
    """

class AVRFCMActionSleep(BaseModel):
    seconds: int
    """
    The number of seconds to sleep for.
    """

class AVRFCMActionTakeoff(BaseModel):
    """
    The altitude to climb to after takeoff.
    """

    rel_alt: float
    """
    Altitude relative to takeoff altitude in meters.
    """

class AVRFCMGoToGlobal(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    """
    Latitude in degrees.
    """
    lon: float = Field(..., ge=-180, le=180)
    """
    Longitude in degrees.
    """
    abs_alt: float
    """
    Absolute altitude in meters.
    """
    hdg: Optional[float]
    """
    Heading in degrees.
    """

class AVRFCMGoToLocal(BaseModel):
    """
    Position to go to in local coordinates. If `d` or `hdg` are omitted, the current position value will be used instead. If `relative` is omitted, the coordinates are assumed to absolute (relative to the home position).
    """

    n: float
    """
    X position in a North/East/Down coordinate system in meters.
    """
    e: float
    """
    Y position in a North/East/Down coordinate system in meters.
    """
    d: Optional[float]
    """
    Z position in a North/East/Down coordinate system in meters.
    """
    hdg: Optional[float]
    """
    Heading in degrees.
    """
    relative: bool = Field(default=False)
    """
    Whether or not the given values are relative to the drone's current position
    """

class AVRFCMMissionUploadWaypoints(BaseModel):
    waypoint_type: Literal["TAKEOFF", "GOTO", "LAND"]
    """
    What kind of waypoint this is
    """
    n: Optional[float]
    """
    X position in a North/East/Down coordinate system in meters.
    """
    e: Optional[float]
    """
    Y position in a North/East/Down coordinate system in meters.
    """
    d: Optional[float]
    """
    Z position in a North/East/Down coordinate system in meters.
    """
    lat: Optional[float] =  Field(..., ge=-90, le=90)
    """
    Latitude in degrees.
    """
    lon: Optional[float] =  Field(..., ge=-180, le=180)
    """
    Longitude in degrees.
    """
    abs_alt: Optional[float]
    """
    Absolute altitude in meters.
    """

class AVRFCMMissionUpload(BaseModel):
    """
    A list of the waypoints for this mission
    """

    waypoints: List[AVRFCMMissionUploadWaypoints]
    """
    Either `n`, `e`, and `d` must be provided, or `lat`, `lon`, and `abs_alt` must be provided. `n`, `e` and `d` represent local coordinates, while `lat`, `lon`, and `abs_alt` represent global (GPS) coordinates. Only the first waypoint may be a "TAKEOFF" waypoint, and that waypoint may omit an X and Y coordinate.
    """

class AVRFCMHILGPSStats(BaseModel):
    frames: int
    """
    The number of messages that have been sent to the flight controller since the software has started.
    """

class AVRFCMAirborne(BaseModel):
    airborne: bool
    """
    Whether the drone is currently airborne or not.
    """

class AVRFCMLanded(BaseModel):
    landed: Literal["UNKNOWN", "ON_GROUND", "IN_AIR", "TAKING_OFF", "LANDING"]
    """
    Landed state of the drone.
    """

class AVRFCMBattery(BaseModel):
    voltage: float
    """
    Battery voltage.
    """
    state_of_charge: float = Field(..., ge=0, le=100)
    """
    Battery state of charge as a percentage
    """

class AVRFCMArmed(BaseModel):
    armed: bool
    """
    Indicates if the drone is currently armed
    """

class AVRFCMFlightMode(BaseModel):
    flight_mode: Literal["UNKNOWN", "READY", "TAKEOFF", "HOLD", "MISSION", "RETURN_TO_LAUNCH", "LAND", "OFFBOARD", "FOLLOW_ME", "MANUAL", "ALTCTL", "POSCTL", "ACRO", "STABILIZED", "RATTITUDE"]
    """
    Active flight mode
    """

class AVRFCMPositionLocal(BaseModel):
    """
    The local position of the drone.
    """

    n: float
    """
    X position in a North/East/Down coordinate system in meters.
    """
    e: float
    """
    Y position in a North/East/Down coordinate system in meters.
    """
    d: float
    """
    Z position in a North/East/Down coordinate system in meters.
    """

class AVRFCMPositionGlobal(BaseModel):
    """
    The global position of the drone.
    """

    lat: float = Field(..., ge=-90, le=90)
    """
    Latitude in degrees.
    """
    lon: float = Field(..., ge=-180, le=180)
    """
    Longitude in degrees.
    """
    rel_alt: float
    """
    Altitude relative to takeoff altitude in meters.
    """
    abs_alt: float
    """
    Absolute altitude in meters.
    """
    hdg: float
    """
    Heading in degrees.
    """

class AVRFCMPositionHome(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    """
    Latitude in degrees.
    """
    lon: float = Field(..., ge=-180, le=180)
    """
    Longitude in degrees.
    """
    rel_alt: float
    """
    Altitude relative to the home position in meters.
    """
    abs_alt: float
    """
    Absolute altitude in meters.
    """

class AVRFCMAttitudeEulerDegrees(BaseModel):
    roll: float = Field(..., ge=-360, le=360)
    """
    Roll in degrees.
    """
    pitch: float = Field(..., ge=-360, le=360)
    """
    Pitch in degrees.
    """
    yaw: float = Field(..., ge=-360, le=360)
    """
    Yaw in degrees.
    """

class AVRFCMVelocity(BaseModel):
    Vn: float
    """
    X velocity in a North/East/Down coordinate system in meters per second.
    """
    Ve: float
    """
    Y velocity in a North/East/Down coordinate system in meters per second.
    """
    Vd: float
    """
    Z velocity in a North/East/Down coordinate system in meters per second.
    """

class AVRFCMGPSInfo(BaseModel):
    visible_satellites: int
    """
    Number of visible satellites in use. HIL GPS will appear as 13.
    """
    fix_type: Literal["NO_GPS", "NO_FIX", "FIX_2D", "FIX_3D", "FIX_DGPS", "RTK_FLOAT", "RTK_FIXED"]
    """
    GPS fix type
    """

class AVRFusionPositionLocal(BaseModel):
    """
    The local position of the drone.
    """

    n: float
    """
    X position in a North/East/Down coordinate system in meters.
    """
    e: float
    """
    Y position in a North/East/Down coordinate system in meters.
    """
    d: float
    """
    Z position in a North/East/Down coordinate system in meters.
    """

class AVRFusionVelocity(BaseModel):
    Vn: float
    """
    X velocity in a North/East/Down coordinate system in meters per second.
    """
    Ve: float
    """
    Y velocity in a North/East/Down coordinate system in meters per second.
    """
    Vd: float
    """
    Z velocity in a North/East/Down coordinate system in meters per second.
    """

class AVRFusionPositionGlobal(BaseModel):
    """
    The global position of the drone.
    """

    lat: float = Field(..., ge=-90, le=90)
    """
    Latitude in degrees.
    """
    lon: float = Field(..., ge=-180, le=180)
    """
    Longitude in degrees.
    """
    alt: float
    """
    Altitude relative to takeoff altitude in meters.
    """

class AVRFusionGroundspeed(BaseModel):
    groundspeed: float
    """
    Groundspeed of the drone in meters per second. This is a normal vector of the N and E velocities.
    """

class AVRFusionHeading(BaseModel):
    hdg: float
    """
    Heading in degrees.
    """

class AVRFusionCourse(BaseModel):
    course: float = Field(..., ge=0, le=360)
    """
    Course in degrees.
    """

class AVRFusionClimbRate(BaseModel):
    climb_rate: float
    """
    Rate of climb in feet per minute.
    """

class AVRFusionAttitudeQuaternion(BaseModel):
    x: float = Field(..., ge=-1, le=1)
    """
    Quaternion x value.
    """
    y: float = Field(..., ge=-1, le=1)
    """
    Quaternion y value.
    """
    z: float = Field(..., ge=-1, le=1)
    """
    Quaternion z value.
    """
    w: float = Field(..., ge=-1, le=1)
    """
    Quaternion w value.
    """

class AVRFusionAttitudeEulerRadians(BaseModel):
    psi: float = Field(..., ge=-6.2831853, le=6.2831853)
    """
    Roll in radians.
    """
    theta: float = Field(..., ge=-6.2831853, le=6.2831853)
    """
    Pitch in radians.
    """
    phi: float = Field(..., ge=-6.2831853, le=6.2831853)
    """
    Yaw in radians.
    """

class AVRFusionHILGPSMessage(BaseModel):
    time_usec: int
    """
    UNIX epoch timestamp in microseconds
    """
    fix_type: int = Field(..., ge=0, le=3)
    """
    0-1: no fix, 2: 2D fix, 3: 3D fix
    """
    lat: int
    """
    WGS84 Latitude * 10000000
    """
    lon: int
    """
    WGS84 Longitude * 10000000
    """
    alt: int
    """
    Altitude from sea level in mm. Positive for up.
    """
    eph: int
    """
    GPS HDOP (horizontal dilution of position)
    """
    epv: int
    """
    GPS VDOP (vertical dilution of position)
    """
    vel: int
    """
    GPS ground speed in centimeters per second
    """
    vn: int
    """
    GPS velocity in north direction in centimeters per second
    """
    ve: int
    """
    GPS velocity in east direction in centimeters per second
    """
    vd: int
    """
    GPS velocity in down direction in centimeters per second
    """
    cog: int
    """
    Course over ground in degrees
    """
    satellites_visible: int = Field(..., ge=0)
    """
    Number of satellites visible. This is hardcoded to 13 for our HIL GPS.
    """
    heading: int
    """
    Custom heading field. This is the heading in degrees * 100.
    """

class AVRVIOResync(BaseModel):
    """
    Position *difference* of the drone, from where the drone thinks it is, to where it really is.
    """

    hdg: float
    """
    Heading in degrees.
    """
    n: float
    """
    X position in a North/East/Down coordinate system in meters.
    """
    e: float
    """
    Y position in a North/East/Down coordinate system in meters.
    """
    d: float
    """
    Z position in a North/East/Down coordinate system in meters.
    """

class AVRVIOPositionLocal(BaseModel):
    """
    Local position of the drone.
    """

    n: float
    """
    X position in a North/East/Down coordinate system in meters.
    """
    e: float
    """
    Y position in a North/East/Down coordinate system in meters.
    """
    d: float
    """
    Z position in a North/East/Down coordinate system in meters.
    """

class AVRVIOVelocity(BaseModel):
    Vn: float
    """
    X velocity in a North/East/Down coordinate system in meters per second.
    """
    Ve: float
    """
    Y velocity in a North/East/Down coordinate system in meters per second.
    """
    Vd: float
    """
    Z velocity in a North/East/Down coordinate system in meters per second.
    """

class AVRVIOAttitudeEulerRadians(BaseModel):
    psi: float = Field(..., ge=-6.2831853, le=6.2831853)
    """
    Roll in radians.
    """
    theta: float = Field(..., ge=-6.2831853, le=6.2831853)
    """
    Pitch in radians.
    """
    phi: float = Field(..., ge=-6.2831853, le=6.2831853)
    """
    Yaw in radians.
    """

class AVRVIOAttitudeQuaternion(BaseModel):
    x: float = Field(..., ge=-1, le=1)
    """
    Quaternion x value.
    """
    y: float = Field(..., ge=-1, le=1)
    """
    Quaternion y value.
    """
    z: float = Field(..., ge=-1, le=1)
    """
    Quaternion z value.
    """
    w: float = Field(..., ge=-1, le=1)
    """
    Quaternion w value.
    """

class AVRVIOHeading(BaseModel):
    hdg: float
    """
    Heading in degrees.
    """

class AVRVIOConfidence(BaseModel):
    tracking: float = Field(..., ge=0, le=100)
    """
    Tracking confidence percentage. Higher number is better.
    """

class AVRVIOImageCaptureShapeItem(PydanticRootModel):
    root: int = Field(..., ge=1)

    def __int__(self) -> int:
        return self.root


class AVRVIOImageCapture(BaseModel):
    data: str
    """
    Base64 encoded data of the image. To reconstruct this as a numpy array,
use `bell.avr.utils.images.deserialize_image` and an `bell.avr.utils.images.ImageData` class.
Alternatively, manually reconstructing the image is as follows:

```python
import base64
import zlib
import numpy as np

image_bytes = base64.b64decode(image_data.encode("utf-8"))

if compressed:
    image_bytes = zlib.decompress(image_bytes)

image_byte_array = bytearray(image_bytes)
image_array = np.array(image_byte_array)

original_array = np.reshape(image_array, shape)
```

    """
    side: Literal["left", "right"]
    """
    Which side of the camera to capture an image from
    """
    if TYPE_CHECKING:
        shape: List[int]
    else:
        shape: List[AVRVIOImageCaptureShapeItem]
    """
    The shape of the image data. For example: [1270, 480, 4] would be a 1270x480 image with 4 channels per pixel.
    """
    @field_validator('shape')
    def _validate_shape(cls, v) -> list: # pyright: ignore
        # Function to convert list of objects into simpler types
        return _convert_type(v, list, int)

    compressed: bool
    """
    Whether or not the image data is zlib compressed.
    """

class AVRVIOImageRequest(BaseModel):
    side: Literal["left", "right"]
    """
    Which side of the camera to capture an image from
    """
    compressed: bool = Field(default=False)
    """
    Whether or not the image data should be zlib compressed.
    """

class AVRVIOImageStreamEnable(BaseModel):
    side: Literal["left", "right"]
    """
    Which side of the camera to capture an image from
    """
    compressed: bool = Field(default=False)
    """
    Whether or not the image data should be zlib compressed.
    """
    frequency: float = Field(..., gt=0, le=5)
    """
    At what rate should new images be sent (frames per second).
    """

class AVRAprilTagsVehiclePosition(BaseModel):
    """
    Position of the drone relative to the world origin in world frame.
    """

    tag_id: int = Field(..., ge=0)
    """
    AprilTag ID.
    """
    x: float
    """
    X position in a North/East/Down coordinate system in centimeters.
    """
    y: float
    """
    Y position in a North/East/Down coordinate system in centimeters.
    """
    z: float
    """
    Z position in a North/East/Down coordinate system in centimeters.
    """
    hdg: float
    """
    Heading in degrees.
    """

class AVRAprilTagsRawApriltagsRotationItem(PydanticRootModel):
    root: float = Field(..., ge=-1, le=1)

    def __float__(self) -> float:
        return self.root


class AVRAprilTagsRawApriltags(BaseModel):
    tag_id: int = Field(..., ge=0)
    """
    AprilTag ID.
    """
    x: float
    """
    The position in meters of the camera relative to the AprilTag's X frame.
    """
    y: float
    """
    The position in meters of the camera relative to the AprilTag's Y frame.
    """
    z: float
    """
    The position in meters of the camera relative to the AprilTag's Z frame.
    """
    if TYPE_CHECKING:
        rotation: Tuple[Tuple[float, float, float], Tuple[float, float, float], Tuple[float, float, float]]
    else:
        rotation: conlist(conlist(AVRAprilTagsRawApriltagsRotationItem, min_length=3, max_length=3), min_length=3, max_length=3)
    """
    3x3 rotation matrix.
    """
    @field_validator('rotation')
    def _validate_rotation(cls, v) -> tuple: # pyright: ignore
        # Function to convert list of objects into simpler types
        return _convert_type(v, tuple, float)


class AVRAprilTagsRaw(BaseModel):
    apriltags: List[AVRAprilTagsRawApriltags]

class AVRAprilTagsVisibleApriltagsAbsolutePosition(BaseModel):
    """
    The position of the drone in world frame in centimeters. If the tag has no truth data, this will not be present in the output.
    """

    x: float
    """
    X position in a North/East/Down coordinate system in centimeters.
    """
    y: float
    """
    Y position in a North/East/Down coordinate system in centimeters.
    """
    z: float
    """
    Z position in a North/East/Down coordinate system in centimeters.
    """

class AVRAprilTagsVisibleApriltagsRelativePosition(BaseModel):
    """
    The relative position of the drone relative to the AprilTag in world frame in centimeters.
    """

    x: float
    """
    X position in a North/East/Down coordinate system in centimeters.
    """
    y: float
    """
    Y position in a North/East/Down coordinate system in centimeters.
    """
    z: float
    """
    Z position in a North/East/Down coordinate system in centimeters.
    """

class AVRAprilTagsVisibleApriltags(BaseModel):
    tag_id: int = Field(..., ge=0)
    """
    AprilTag ID.
    """
    horizontal_distance: float
    """
    The horizontal scalar distance from the drone to AprilTag, in centimeters.
    """
    vertical_distance: float
    """
    The horizontal scalar distance from the drone to AprilTag, in centimeters.
    """
    angle: float
    """
    The angle formed by the vector pointing from the drones body to the AprilTag in world frame relative to world-north.
    """
    hdg: float
    """
    Heading in degrees.
    """
    relative_position: AVRAprilTagsVisibleApriltagsRelativePosition
    """
    The relative position of the drone relative to the AprilTag in world frame in centimeters.
    """
    absolute_position: Optional[AVRAprilTagsVisibleApriltagsAbsolutePosition]
    """
    The position of the drone in world frame in centimeters. If the tag has no truth data, this will not be present in the output.
    """

class AVRAprilTagsVisible(BaseModel):
    apriltags: List[AVRAprilTagsVisibleApriltags]

class AVRAprilTagsStatus(BaseModel):
    frames_per_second: int = Field(..., ge=0)
    """
    Number of frames of video data processed in the last second
    """

class AVRThermalReadingShapeItem(PydanticRootModel):
    root: int = Field(..., ge=1)

    def __int__(self) -> int:
        return self.root


class AVRThermalReading(BaseModel):
    data: str
    """
    Base64 encoded data of the image. To reconstruct this as a numpy array,
use `bell.avr.utils.images.deserialize_image` and an `bell.avr.utils.images.ImageData` class.
Alternatively, manually reconstructing the image is as follows:

```python
import base64
import zlib
import numpy as np

image_bytes = base64.b64decode(image_data.encode("utf-8"))

if compressed:
    image_bytes = zlib.decompress(image_bytes)

image_byte_array = bytearray(image_bytes)
image_array = np.array(image_byte_array)

original_array = np.reshape(image_array, shape)
```

    """
    if TYPE_CHECKING:
        shape: List[int]
    else:
        shape: List[AVRThermalReadingShapeItem]
    """
    The shape of the image data. For example: [1270, 480, 4] would be a 1270x480 image with 4 channels per pixel.
    """
    @field_validator('shape')
    def _validate_shape(cls, v) -> list: # pyright: ignore
        # Function to convert list of objects into simpler types
        return _convert_type(v, list, int)

    compressed: bool
    """
    Whether or not the image data is zlib compressed.
    """

class AVRAutonomousBuildingEnable(BaseModel):
    building: int = Field(..., ge=0, le=15)
    """
    Building ID. This is 0-indexed.
    """

class AVRAutonomousBuildingDisable(BaseModel):
    building: int = Field(..., ge=0, le=15)
    """
    Building ID. This is 0-indexed.
    """

class _AVRFCMGPSInfoCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFCMGPSInfo) -> Any:
        ...

class _AVRFCMArmedCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFCMArmed) -> Any:
        ...

class _AVRPCMColorTimedCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRPCMColorTimed) -> Any:
        ...

class _AVRVIOAttitudeEulerRadiansCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRVIOAttitudeEulerRadians) -> Any:
        ...

class _AVREmptyMessageCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self) -> Any:
        ...

class _AVRPCMServoPercentCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRPCMServoPercent) -> Any:
        ...

class _AVRVIOImageCaptureCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRVIOImageCapture) -> Any:
        ...

class _AVRVIOImageRequestCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRVIOImageRequest) -> Any:
        ...

class _AVRFusionClimbRateCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFusionClimbRate) -> Any:
        ...

class _AVRFusionPositionGlobalCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFusionPositionGlobal) -> Any:
        ...

class _AVRVIOVelocityCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRVIOVelocity) -> Any:
        ...

class _AVRFCMMissionUploadCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFCMMissionUpload) -> Any:
        ...

class _AVRFCMHILGPSStatsCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFCMHILGPSStats) -> Any:
        ...

class _AVRPCMColorSetCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRPCMColorSet) -> Any:
        ...

class _AVRVIOAttitudeQuaternionCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRVIOAttitudeQuaternion) -> Any:
        ...

class _AVRAutonomousBuildingEnableCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRAutonomousBuildingEnable) -> Any:
        ...

class _AVRFCMAirborneCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFCMAirborne) -> Any:
        ...

class _AVRFCMBatteryCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFCMBattery) -> Any:
        ...

class _AVRAprilTagsVehiclePositionCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRAprilTagsVehiclePosition) -> Any:
        ...

class _AVRPCMServoAbsoluteCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRPCMServoAbsolute) -> Any:
        ...

class _AVRFCMPositionHomeCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFCMPositionHome) -> Any:
        ...

class _AVRAprilTagsStatusCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRAprilTagsStatus) -> Any:
        ...

class _AVRFCMPositionLocalCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFCMPositionLocal) -> Any:
        ...

class _AVRAutonomousBuildingDisableCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRAutonomousBuildingDisable) -> Any:
        ...

class _AVRFusionGroundspeedCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFusionGroundspeed) -> Any:
        ...

class _AVRPCMServoPWMCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRPCMServoPWM) -> Any:
        ...

class _AVRFCMActionSleepCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFCMActionSleep) -> Any:
        ...

class _AVRFCMVelocityCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFCMVelocity) -> Any:
        ...

class _AVRThermalReadingCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRThermalReading) -> Any:
        ...

class _AVRFCMAttitudeEulerDegreesCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFCMAttitudeEulerDegrees) -> Any:
        ...

class _AVRFCMGoToGlobalCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFCMGoToGlobal) -> Any:
        ...

class _AVRFCMLandedCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFCMLanded) -> Any:
        ...

class _AVRFCMGoToLocalCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFCMGoToLocal) -> Any:
        ...

class _AVRVIOResyncCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRVIOResync) -> Any:
        ...

class _AVRVIOConfidenceCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRVIOConfidence) -> Any:
        ...

class _AVRFusionPositionLocalCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFusionPositionLocal) -> Any:
        ...

class _AVRFCMFlightModeCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFCMFlightMode) -> Any:
        ...

class _AVRFusionHeadingCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFusionHeading) -> Any:
        ...

class _AVRAprilTagsRawCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRAprilTagsRaw) -> Any:
        ...

class _AVRPCMServoCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRPCMServo) -> Any:
        ...

class _AVRFusionAttitudeEulerRadiansCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFusionAttitudeEulerRadians) -> Any:
        ...

class _AVRFusionVelocityCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFusionVelocity) -> Any:
        ...

class _AVRVIOPositionLocalCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRVIOPositionLocal) -> Any:
        ...

class _AVRVIOImageStreamEnableCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRVIOImageStreamEnable) -> Any:
        ...

class _AVRFusionHILGPSMessageCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFusionHILGPSMessage) -> Any:
        ...

class _AVRFCMActionTakeoffCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFCMActionTakeoff) -> Any:
        ...

class _AVRAprilTagsVisibleCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRAprilTagsVisible) -> Any:
        ...

class _AVRVIOHeadingCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRVIOHeading) -> Any:
        ...

class _AVRFusionCourseCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFusionCourse) -> Any:
        ...

class _AVRFusionAttitudeQuaternionCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFusionAttitudeQuaternion) -> Any:
        ...

class _AVRFCMPositionGlobalCallable(Protocol):
    """
    Class used only for type-hinting MQTT callbacks.
    """
    def __call__(self, payload: AVRFCMPositionGlobal) -> Any:
        ...
