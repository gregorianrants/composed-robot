"""
./sonar_ranger.py 1 24 25 # ping gpiochip1: trigger 24, echo 25
./sonar_ranger.py 24 25   # ping gpiochip0: trigger 24, echo 25
"""

import time
import sys
import time
import threading


class Ranger:
    def __init__(self, sbc, chip, trigger, echo, id):
        self._sbc = sbc
        self._chip = chip
        self._trigger = trigger
        self._echo = echo
        self._event = threading.Event()

        self._ping = False
        self._high = None
        self._time = None
        self._id = id

        self._handle = sbc.gpiochip_open(chip)

        sbc.gpio_claim_output(self._handle, trigger)

        sbc.gpio_claim_alert(self._handle, echo, sbc.BOTH_EDGES)

        self._cb = sbc.callback(self._handle, echo, sbc.BOTH_EDGES, self._cbf)

        self._inited = True

    def _cbf(self, chip, gpio, level, tick):
        if level == 1:
            self._high = tick
        else:
            if self._high is not None:
                self._time = tick - self._high
                self._high = None
                self._event.set()

    def read(self):
        if self._inited:
            self._event.clear()
            self._time = None
            # send a 15 microsecond high pulse as trigger
            self._sbc.tx_pulse(self._handle, self._trigger, 15, 0, 0, 1)
            start = time.time()
            self._event.wait(timeout=0.3)
            if self._time == None:
                self._time = 0.3
            # TODO sometimes when sensor is playing up i get a reading of close to 0
            # havent figured out why this happens from point of view of code have put a hack in to replace with big value and rely on the other sensors when this happens
            # otherwise behaves as if really close to something and goes potty.

            distance = 17015 * self._time / 1e9
            if distance < 0.001:
                distance = 500
            return {
                "id": self._id,
                # "distance": "{:.1f}".format(17015 * self._time / 1e9),
                "distance": (17015 * self._time / 1e9),
            }

        else:
            return None

    def cancel(self):
        if self._inited:
            self._inited = False
            self._cb.cancel()
            self._sbc.gpio_free(self._chip, self._trigger)
            self._sbc.gpio_free(self._chip, self._echo)
            self._sbc.gpiochip_close(self._chip)
