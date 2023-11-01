from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame

def play_audio():
    pygame.init()

    try:
        pygame.mixer.music.load('assets/pikmin.wav')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except pygame.error as e:
        print(f"An error occurred: {e}")
    finally:
        pygame.quit()

def main():
    play_audio()    
    
if __name__ == "__main__":
    main()