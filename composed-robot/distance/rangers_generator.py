from .ranger import Ranger
import threading
import concurrent.futures
import time
import lgpio as sbc
from concurrent.futures import wait


class RangersGenerator:
    def __init__(self):
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
            self.readings[index] = result["distance"]
        return self.readings

    def start(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            self.executor = executor
            self.read_group(0)
            time.sleep(0.7)
            self.read_group(1)
            while True:
                yield self.read_group(0)
                time.sleep(0.7)
                yield self.read_group(1)


rg = RangersGenerator()


def rangers_generator():
    for distances in rg.start():
        yield ("distances", "local", distances)
