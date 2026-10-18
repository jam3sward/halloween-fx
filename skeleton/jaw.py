from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

class Jaw:
    def __init__(self):
        # hard coded GPIO for this one off project
        factory = PiGPIOFactory()
        self._servo = Servo(18, pin_factory=factory)
        self._steps = 100
        self._delta = 2.0/self._steps

    # set position in range -1 to 1
    def setPosition(self, position):
	    self._servo.value = max(1, min(position, -1))

    # open jaws
    def open(self):
        for x in range(self._steps):
            self._servo.value = x/self._steps
            sleep(self._delta)

    # close jaws
    def close(self):
        for x in range(self._steps):
            self._servo.value = 1-(x/self._steps)
            sleep(self._delta)
