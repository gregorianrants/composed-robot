from .ranger import Ranger
import threading
import concurrent.futures
import time
import lgpio as sbc
from concurrent.futures import wait
from robonet.Publisher import Publisher
from dotenv import load_dotenv
import zmq
import os

load_dotenv()


PI_IP = os.getenv("PI_IP")


class Rangers:
    def __init__(self, cb):
        # self.rangers = [
        #     Ranger(sbc, 0, 26, 19, 0),
        #     Ranger(sbc, 0, 21, 20, 1),
        #     Ranger(sbc, 0, 6, 12, 2),
        #     Ranger(sbc, 0, 23, 24, 3),
        #     Ranger(sbc, 0, 27, 22, 4),
        # ]
        self.rangers = [
             Ranger(sbc, 0, 27, 22, 4),
             Ranger(sbc, 0, 23, 24, 3),
              Ranger(sbc, 0, 6, 12, 2),
              Ranger(sbc, 0, 21, 20, 1),
              Ranger(sbc, 0, 26, 19, 0),
        ]
        self.groups = [[0, 2, 4], [1, 3]]
        self.executor = None
        self.cb = cb
        self.readings = [None] * 5

    def get_group(self, index):
        return [self.rangers[i] for i in self.groups[index]]

    def read_group(self, group_index):
        futures = [
            self.executor.submit(ranger.read) for ranger in self.get_group(group_index)
        ]
        wait(futures)
        results = [f.result() for f in futures]
        for result in results:
            index = result["id"]
            self.readings[index] = result['distance']
        self.cb(self.readings)

    def start(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            self.executor = executor
            for i in range(100):
                self.read_group(0)
                time.sleep(0.7)
                self.read_group(1)
                time.sleep(0.7)


context = zmq.Context()

time.sleep(1)

publisher = Publisher(
    hub_ip=PI_IP,
    context=context,
    address=f"tcp://{PI_IP}",
    node="distances",
    topics=["distances"],
)


def send_json(distances):
    publisher.send_json("distances", distances)


rangers = Rangers(send_json)
rangers.start()
