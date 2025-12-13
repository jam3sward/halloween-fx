from time import sleep
import pygame
import pygame._sdl2.audio as sdl2_audio

class Audio:
    def get_audio_devices(self) -> tuple[str, ...]:
        devices = tuple(sdl2_audio.get_audio_device_names(False))
        return devices
    
    def __init__(self):
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=2048)
        pygame.mixer.init()
        
        devices = self.get_audio_devices()
        
        print(devices)
        if not devices:
            raise RuntimeError("no audio device")
        
        pygame.mixer.init(devicename=devices[0])
    
    def __del__(self):
        pygame.mixer.quit()
    
    def play(self, file_path: str):
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.get_busy():
            sleep(0.1)
    