import time
from robonet.Publisher import Publisher
from dotenv import load_dotenv
import zmq
import os
from .rangers import Rangers

load_dotenv()


PI_IP = os.getenv("PI_IP")

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
