import pigpio
import hcsr04
import time
import pygame
import smoke
import random

# Range finder 0
RANGER0_TRIG_OP = 14    # range finder trigger output
RANGER0_ECHO_IP = 15    # range finder echo input

# Range finder 1
RANGER1_TRIG_OP = 23    # range finder trigger output
RANGER1_ECHO_IP = 24    # range finder echo input

# Smoke machine
SMOKE_MACHINE_OP = 25   # smoke machine output

# Path to sound effect files
SOUND_PATH = "sounds/"

_debugOutput = True
_rangeThreshold0 = 1.2
_rangeThreshold1 = 1.2
_smokeTimeOn = 1.0
_smokeTimeOff = 4.0
_ambientDuration = 1 * 60 * 1000 # ambient sound duration (ms)

_channelRoar = None
_channelAmbient = None

_ambientStart = None

def setupRangers():
    global _ranger0
    _ranger0 = hcsr04.Ranger(RANGER0_TRIG_OP, RANGER0_ECHO_IP)
    global _ranger1
    _ranger1 = hcsr04.Ranger(RANGER1_TRIG_OP, RANGER1_ECHO_IP)

def cleanupRangers():
    _ranger0.cleanup()
    _ranger1.cleanup()

def setupSound():
    print("audio init")
    # initialise the mixer
    # 44.1kHz, signed 16-bit, 1 channel, 4096 buffer size
    pygame.mixer.init(44100,-16,1,32768)

    # load our sound samples
    global _soundRoar
    _soundRoar = {}
    _soundRoar[0] = pygame.mixer.Sound(SOUND_PATH + "roar1.wav")
    _soundRoar[1] = pygame.mixer.Sound(SOUND_PATH + "roar2.wav")
    _soundRoar[2] = pygame.mixer.Sound(SOUND_PATH + "roar3.wav")

    global _soundStartup
    _soundStartup = pygame.mixer.Sound(SOUND_PATH + "startup.wav")

    global _soundAmbient
    _soundAmbient = pygame.mixer.Sound(SOUND_PATH + "ambient.wav")
    print("audio ready")

def setup():
    # set up the range finders
    setupRangers()

    # set up the sound samples
    setupSound()

    # initialise PIGPIO
    global _gpio
    _gpio = pigpio.pi()

    # initialise smoke machine
    global _smoke
    _smoke = smoke.Smoke(SMOKE_MACHINE_OP)

def cleanup():
    cleanupRangers()

    global _smoke
    _smoke.cleanup()
    _smoke = None

def startSmokeMachine(duration):
    if _smoke.activate(duration):
        if _debugOutput:
            print("start smoke machine for", duration, "s")

def startRoar():
    if _debugOutput:
        print("start sound effect")

    global _channelRoar
    #if _channelRoar and _channelRoar.get_busy():
    #    print("** channel busy **")
    #    return

    _channelRoar = _soundRoar[random.randrange(3)].play()
    _channelRoar.set_volume(1)

def ambientStart():
    print("start ambient sound")

    global _channelAmbient
    if _channelAmbient and _channelAmbient.get_busy():
        return

    _channelAmbient = _soundAmbient.play()
    _channelAmbient.set_volume(0.5)

    global _ambientStart
    _ambientStart = time.time()

def ambientUpdate():
    now = time.time()
    global _ambientStart
    global _ambientDuration
    if _ambientStart and now - _ambientStart > _ambientDuration:
        print("stopping ambient")
        _channelAmbient.fadeout(2000)  # blocks
        _ambientStart = None

def startupSound():
    global _channelRoar
    _channelRoar = _soundStartup.play()

def main():
    print("starting")
    setup()

    startupSound()

    # ignore values below this distance
    minRangeFilter = 0.2
    lastBreach = time.time()

    print("running")

    while True or pygame.mixer.get_busy():
        if not _ambientStart:
            range0 = _ranger0.getRange()
            if range0 > minRangeFilter and range0 < _rangeThreshold0:
                print("breach range 0 =", round(range0,2), "m")
                ambientStart()

        range1 = _ranger1.getRange()
        timeNow = time.time()

        if range1 > minRangeFilter and range1 < _rangeThreshold1:
            if timeNow - lastBreach > 2:
                print("breach range 1 =", round(range1,2), "m")
                startRoar()
                startSmokeMachine(3.0)
                lastBreach = time.time()

        global _smoke
        _smoke.update()
        ambientUpdate()

    print("exiting")
    cleanup()

# if we are run as the main script
if __name__=="__main__":
    # enter the main function
    main()
