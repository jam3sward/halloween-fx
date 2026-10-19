from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

# to suit TowerPro MG995 with 180 degree range
min_servo_pulse_width = 0.5/1000.0
max_servo_pulse_width = 2.5/1000.0

class Jaw:
    def __init__(self):
        # pigpio pin factory to use hardware PWM
        # and avoid servo jitter
        factory = PiGPIOFactory()

        # hard coded GPIO for this one off project
        self._servo = Servo(18,
            min_pulse_width=min_servo_pulse_width,
            max_pulse_width=max_servo_pulse_width,
            pin_factory=factory)

        # interpolation steps
        self._steps = 100
        # time delay per step
        self._delta = 1.0/self._steps
        # range of motion
        self._range = 0.8

    # open jaws
    def open(self):
        for x in range(self._steps):
            self._servo.value = -self._range*x/self._steps
            sleep(self._delta)

    # close jaws
    def close(self):
        for x in range(self._steps):
            self._servo.value = self._range*(-1+x/self._steps)
            sleep(self._delta)
