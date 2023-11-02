from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import pkg_resources
from colorama import Fore
from pikmin.art import ascii

def play_audio():
    # asset_path = pkg_resources.resource_filename('pikmin', 'assets/pikmin.wav')
    asset_path = pkg_resources.resource_filename('pikmin', 'assets/pikmin.wav')

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
    print(Fore.RED, ascii)
    play_audio()
    
if __name__ == "__main__":
    main()