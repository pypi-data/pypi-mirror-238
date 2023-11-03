from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import pyautogui as pg
import webbrowser
import pkg_resources
import moviepy.editor as mp
from termcolor import colored

def play_video():
    easter_video_path = pkg_resources.resource_filename('arpit', 'assets/easter_video.mp4')
    easter_audio_path = pkg_resources.resource_filename('arpit', 'assets/easter_audio.mp3')
    
    video_clip = mp.VideoFileClip(easter_video_path)
    audio_clip = mp.AudioFileClip(easter_audio_path)

    video_clip = video_clip.set_audio(audio_clip)

    video_clip.preview(fps=25)
    
def play_audio(path='assets/audio.ogg'):
    cassete_path = pkg_resources.resource_filename('arpit', path)

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
    
    will_you_text = colored('Will you? ', 'red', attrs=['reverse', 'blink'])
    print(will_you_text, end=" ")
    
    pg.hotkey('alt', 'tab')
    user_input = input()
    if user_input.lower() in ["yes", "y"]:
        play_audio('assets/yes_audio.mp3')
        webbrowser.open('https://www.linktr.ee/arpy8')
    elif user_input.lower() in ["no", "n"]:
        play_audio('assets/no_audio.mp3')
        
if __name__ == "__main__":
    main()