from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import time
import pygame
import pkg_resources
import moviepy.editor as mp
from colorama import Fore, init

def play_video():
    easter_video_path = pkg_resources.resource_filename('arpit', 'assets/easter_video.mp4')
    easter_audio_path = pkg_resources.resource_filename('arpit', 'assets/easter_audio.mp3')
    
    video_clip = mp.VideoFileClip(easter_video_path)
    audio_clip = mp.AudioFileClip(easter_audio_path)

    video_clip = video_clip.set_audio(audio_clip)

    video_clip.preview(fps=25)
    
def play_audio():
    cassete_path = pkg_resources.resource_filename('arpit', 'assets/audio.ogg')

    try:
        pygame.init()
        pygame.mixer.music.load(cassete_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except pygame.error as e:
        print(f"An error occurred: {e}")
    finally:
        pygame.quit()

def main():
    play_video()
    # print(Fore.GREEN, "Loading cassete...")
    # time.sleep(0.3)
    # play_audio()
    # print(Fore.RED, "Exiting, empty cassete detected.")
    
    
if __name__ == "__main__":
    main()