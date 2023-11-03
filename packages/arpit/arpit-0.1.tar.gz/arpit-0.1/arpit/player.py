from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import time
import pygame
import pkg_resources
from colorama import Fore, init

init(autoreset=True)

def play_audio():
    asset_path = pkg_resources.resource_filename('arpit', 'assets/audio.ogg')

    try:
        pygame.init()
        pygame.mixer.music.load(asset_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except pygame.error as e:
        print(f"An error occurred: {e}")
    finally:
        pygame.quit()

def main():
    print(Fore.GREEN, "Loading cassete...")
    time.sleep(0.3)
    play_audio()
    print(Fore.RED, "Exiting, empty cassete detected.")
    
    
if __name__ == "__main__":
    main()