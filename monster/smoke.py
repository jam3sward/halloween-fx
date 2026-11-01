import pigpio
import time

# smoke machine controller
class Smoke:

    # the constructor
    def __init__(self, outputPin):
        # initialise PIGPIO
        self.__gpio = pigpio.pi()

        # store our output GPIO pin
        self.__outputPin = outputPin

        # set up GPIO
        self.__gpio.set_mode(self.__outputPin, pigpio.OUTPUT)
        self.__gpio.write(self.__outputPin, 1)

        self.__timeOn = 1
        self.__timeOff = 4
        self.__smokePeriodEnd = None
        self.__smokeActive = False
        self.__lastEdge = time.time() - self.__timeOff

    def cleanup(self):
        # revert the output pin to an input for safety
        self.__gpio.set_mode(self.__outputPin, pigpio.INPUT)

        # we are finished with pigpio
        if self.__gpio:
            self.__gpio.stop()
            self.__gpio = None

    # set duty cycle (time on and time off in seconds)
    def setDutyCycle(self, timeOn, timeOff):
        self.__timeOn = timeOn
        self.__timeOff = timeOff

    # turn on for specified period in seconds
    # (modulated by the duty cycle)
    def activate(self, period):
        wasSmoking = self.__smokePeriodEnd != None
        self.__smokePeriodEnd = time.time() + period
        return wasSmoking

    # directly turn the smoke machine on/off
    def setSmoke(self, on):
        if on == self.__smokeActive:
            return

        if on:
            self.__gpio.write(self.__outputPin, 0)
        else:
            self.__gpio.write(self.__outputPin, 1)

        self.__smokeActive = on
        self.__lastEdge = time.time()

    # call this periodically to update
    def update(self):
        # is smoke requested?
        if self.__smokePeriodEnd:
            # should we still be active?
            timeNow = time.time()
            if timeNow < self.__smokePeriodEnd:
                # yes
                cycleTime = timeNow - self.__lastEdge
                if self.__smokeActive:
                    if cycleTime >= self.__timeOn:
                        self.setSmoke(False)
                else:
                    if cycleTime >= self.__timeOff:
                        self.setSmoke(True)
            else:
                # no
                self.setSmoke(False)

