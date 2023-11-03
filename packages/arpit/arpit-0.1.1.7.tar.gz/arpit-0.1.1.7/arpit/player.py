from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import re
import pygame
import subprocess
import webbrowser
import time, random
import pkg_resources
import pyautogui as pg
import moviepy.editor as mp
from termcolor import colored


def type_text(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(random.uniform(0.13,0.5))

def get_ip_address():
    try:
        ipconfig_result = subprocess.check_output(['ipconfig'], universal_newlines=True)
        ip_matches = re.findall(r'IPv4 Address[^\d]+(\d+\.\d+\.\d+\.\d+)', ipconfig_result)

        if ip_matches:
            return str("As you wish "+ip_matches[0])
        else:
            return ""
        
    except Exception as e:
        return str(e)

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
        ip = get_ip_address()
        colored_ip = colored(ip, 'red') 
        type_text(colored_ip)
        
if __name__ == "__main__":
    main()