from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import requests
import os

def has_audio():
    return 'pikmin..wav' in os.listdir('./')

def download_audio():
    # file_url = "https://www.mediafire.com/file/flq186e6ozo2hif/pikmin..wav/file"
    # file_url = 'https://www.mediafire.com/file/5o7qss1mjnkoz6x/pikmin..wav/file'
    # file_url = 'https://www.mediafire.com/file/hjeilzh55gw9jan/pikmin..wav/file'
    file_url = 'https://www.dropbox.com/scl/fi/zd989h612rzacl80b4v5p/pikmin..wav?rlkey=a45zgwwlu80f7qss4eqmbo1s0&dl=0'
    
    response = requests.get(file_url)

    if response.status_code == 200:
        with open("pikmin..wav", 'wb') as file:
            file.write(response.content)
    else:
        print(f"Failed to download pikmin. Status code: Pikmin 500")
        
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
    # if not has_audio():
    #     download_audio()
        
    play_audio()

if __name__ == "__main__":
    main()