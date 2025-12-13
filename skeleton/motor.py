from gpiozero import OutputDevice, InputDevice
import pygame
import time
import math

class Motor:
    def __init__(self):
        # hard coded GPIO for this one off project
        self._motorEnable = OutputDevice(26)
        self._motorPin1   = OutputDevice(5)
        self._motorPin2   = OutputDevice(6)
        self._sensorPin   = InputDevice(17)
        # radius in cm
        radius = 2
        # circumference in cm
        self._circumference = 2 * math.pi * radius
        print(f"pulley circumference = {self._circumference}")

    def setMotor(self, enable, in1, in2):
        self._motorEnable.value = enable
        self._motorPin1.value = in1
        self._motorPin2.value = in2

    def driveSteps(self, dir, steps):
        self.setMotor(1,dir,1-dir)
        count = 0
        while count < steps:
            while not self._sensorPin.value:
                pass
            count += 1
            while self._sensorPin.value:
                pass
        self.stop()

    # drive some distance in cm (rounded up)
    def driveDistance(self, dir, distance):
        steps = math.ceil(distance / self._circumference)
        self.driveSteps(dir, steps)

    def forward(self, steps):
        self.drive(0, steps)

    def back(self, steps):
        self.drive(1, steps)

    def stop(self):
        self.setMotor(0,0,0)
