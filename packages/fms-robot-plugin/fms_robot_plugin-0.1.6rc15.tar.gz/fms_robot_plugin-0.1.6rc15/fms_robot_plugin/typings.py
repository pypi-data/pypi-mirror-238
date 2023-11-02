import enum
import datetime

from typing import List, Union
from pydantic import BaseModel


class TaskType(str, enum.Enum):
    """
    Possible types of tasks in FMS2
    """

    Waypoint = "WAYPOINT"


class ConnectionStatus(str, enum.Enum):
    """
    Status used for indicating the connection of a robot
    """

    Connected = "CONNECTED"
    Disconnected = "DISCONNECTED"
    # Localizing = "LOCALIZING"


class Status(str, enum.Enum):
    """
    This value is derived from actionlib_msgs/GoalStatus
    """

    Pending = "PENDING"
    Active = "ACTIVE"
    Preempted = "PREEMPTED"
    Succeeded = "SUCCEEDED"
    Aborted = "ABORTED"
    Rejected = "REJECTED"
    Preempting = "PREEMPTING"
    Recalling = "RECALLING"
    Recalled = "RECALLED"
    Lost = "LOST"


class Point(BaseModel):
    """
    Based on ROS geometry_msgs/Point
    """

    x: float
    y: float
    z: float


class Vector3(BaseModel):
    """
    Based on ROS geometry_msgs/Vector3
    """

    x: float
    y: float
    z: float


class Quarternion(BaseModel):
    """
    Based on ROS geometry_msgs/Quarternion
    """

    x: float
    y: float
    z: float
    w: float


class Twist(BaseModel):
    """
    Based on ROS geometry_msgs/Twist
    """

    linear: Vector3
    angular: Vector3


class LaserScan(BaseModel):
    """
    Based on ROS sensor_msgs/LaserScan
    """

    angle_min: float
    angle_max: float
    angle_increment: float
    time_increment: float
    scan_time: float
    range_min: float
    range_max: float
    ranges: list[float | None]
    intensities: list[float]


class Pose(BaseModel):
    """
    Based on ROS geometry_msgs/Pose
    """

    position: Point
    orientation: Quarternion


class MapMetadata(BaseModel):
    """
    Based on ROS nav_msgs/MapMetaData
    """

    resolution: float
    width: int
    height: int
    origin: Pose


class Map(BaseModel):
    """
    Contains the basic information of a navigational map
    """

    metadata: MapMetadata
    data: str


class RobotInfo(BaseModel):
    timestamp: datetime.datetime
    id: str
    priority: int
    footprint: List[Point]
    radius: float
    pose: Pose
    velocity: Twist
    pose_covariance: List[int]
    velocity_covariance: List[int]


class Waypoint(BaseModel):
    poses: List[Pose]


class Task(BaseModel):
    id: str
    type: TaskType
    data: Union[Waypoint]
    map_id: str
    linear_velocity: float
    angular_velocity: float
