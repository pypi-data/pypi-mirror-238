from typing import Any, Callable, Optional

import json
import datetime
import paho.mqtt.client as mqtt

from fms_robot_plugin.typings import ConnectionStatus, Status, LaserScan, Twist, Pose, Map, RobotInfo, Task
from fms_robot_plugin.mqtt import MqttClient, MqttConsumer


class Robot:
    robot_key: Optional[str]

    def __init__(
        self,
        robot_key: str,
        broker_host: str = "broker.movelrobotics.com",
        broker_port: int = 1883,
    ):
        self.robot_key = robot_key
        self.priority = None

        self.broker_host = broker_host
        self.broker_port = broker_port
        self.mqtt = MqttClient(broker_host, broker_port)

    def run(self):
        self.register_default_callbacks()
        self.establish_connection()

    """
    Command Callbacks

    These methods are called when a command is published from the FMS server.
    """

    def on_teleop(self, cb: Callable[[Twist], None]):
        topic = f"robots/{self.robot_key}/teleop"
        self.consumer(topic).consume(lambda data: cb(Twist(**data)))

    def on_stop(self, cb: Callable[[], None]):
        topic = f"robots/{self.robot_key}/stop"
        self.consumer(topic).consume(lambda _: cb(), serialize=False)

    def on_start_mapping(self, cb: Callable[[str], None]):
        topic = f"robots/{self.robot_key}/mapping/start"
        self.consumer(topic).consume(lambda map_id: cb(map_id), serialize=False)

    def on_save_mapping(self, cb: Callable[[], None]):
        topic = f"robots/{self.robot_key}/mapping/save"
        self.consumer(topic).consume(lambda _: cb(), serialize=False)

    def on_localize(self, cb: Callable[[str, Pose], None]):
        topic = f"robots/{self.robot_key}/localize"
        self.consumer(topic).consume(lambda data: cb(data["map_id"], Pose(**data["initial_pose"])))

    def on_load_map_pgm(self, cb: Callable[[bytes, str], None]):
        topic = f"robots/{self.robot_key}/maps/:map_id/load/pgm"
        self.consumer(topic).consume(lambda pgm, url_params: cb(pgm, url_params["map_id"]), serialize=False)

    def on_load_map_yaml(self, cb: Callable[[bytes, str], None]):
        topic = f"robots/{self.robot_key}/maps/:map_id/load/yaml"
        self.consumer(topic).consume(lambda yaml, url_params: cb(yaml, url_params["map_id"]), serialize=False)

    def on_unload_map(self, cb: Callable[[], None]):
        topic = f"robots/{self.robot_key}/maps/unload"
        self.consumer(topic).consume(lambda _: cb(), serialize=False)

    def on_execute_task(self, cb: Callable[[Task], None]):
        topic = f"robots/{self.robot_key}/tasks/execute"
        self.consumer(topic).consume(lambda data: cb(Task(**data)))

    def on_resume_task(self, cb: Callable[[], None]):
        topic = f"robots/{self.robot_key}/tasks/resume"
        self.consumer(topic).consume(lambda _: cb(), serialize=False)

    def on_pause_task(self, cb: Callable[[], None]):
        topic = f"robots/{self.robot_key}/tasks/pause"
        self.consumer(topic).consume(lambda _: cb(), serialize=False)

    # TODO: fix the Any typing
    def on_set_priority(self, cb: Callable[[Any], None]):
        topic = f"/robots/{self.robot_key}/priority"
        self.consumer(topic).consume(lambda data: cb(data["priority"]))

    def on_robot_info(self, cb: Callable[[RobotInfo], None]):
        topic = f"robots/{self.robot_key}/info"
        self.consumer(topic).consume(lambda data: cb(RobotInfo(**data)))

    """
    Publishers

    These methods are called to publish data to the FMS server.
    """

    def set_camera_feed(self, data: str):
        self.mqtt.publish(f"robots/{self.robot_key}/camera", data, serialize=False)

    def set_lidar(self, data: LaserScan):
        self.mqtt.publish(f"robots/{self.robot_key}/lidar", data.dict())

    def set_pose(self, data: Pose):
        self.mqtt.publish(f"robots/{self.robot_key}/pose", data.dict())

    def set_map_data(self, data: Map):
        self.mqtt.publish(f"robots/{self.robot_key}/mapping/data", data.dict())

    def set_status(self, data: Status):
        self.mqtt.publish(f"robots/{self.robot_key}/status", data, serialize=False)

    def set_battery_percentage(self, data: float):
        self.mqtt.publish(f"robots/{self.robot_key}/battery", data, serialize=False)

    def set_map_result(self, pgm: bytes, yaml: bytes):
        self.mqtt.publish(f"robots/{self.robot_key}/mapping/result/pgm", pgm, serialize=False)
        self.mqtt.publish(f"robots/{self.robot_key}/mapping/result/yaml", yaml, serialize=False)

    def set_cpu_usage(self, data: float):
        self.mqtt.publish(f"robots/{self.robot_key}/monitor/cpu", data, serialize=False)

    def set_memory_usage(self, data: float):
        self.mqtt.publish(f"robots/{self.robot_key}/monitor/memory", data, serialize=False)

    def set_battery_usage(self, data: float):
        self.mqtt.publish(f"robots/{self.robot_key}/monitor/battery", data, serialize=False)

    def set_robot_info(self, data: RobotInfo):
        self.mqtt.publish(f"robots/{self.robot_key}/info", data.dict())

    """
    Utilities
    """

    def consumer(self, topic: str):
        return MqttConsumer(topic, self.broker_host, self.broker_port)

    def register_default_callbacks(self):
        self.on_set_priority(self.set_priority)

    def set_priority(self, priority):
        self.priority = priority

    def establish_connection(self):
        client = mqtt.Client()
        connection_topic = f"robots/{self.robot_key}/connection"

        def on_connect(client, userdata, flags, rc):
            client.publish(
                connection_topic,
                payload=json.dumps(
                    {"status": ConnectionStatus.Connected.value, "sent_at": datetime.datetime.utcnow().isoformat()}
                ),
            )

        client.on_connect = on_connect
        client.will_set(
            connection_topic,
            payload=json.dumps(
                {
                    "status": ConnectionStatus.Disconnected.value,
                    "sent_at": datetime.datetime.utcnow().isoformat(),
                }
            ),
            qos=0,
            retain=True,
        )

        client.connect(self.broker_host, self.broker_port)
        client.loop_forever()
