import pygame
import os

class MusicPlayer:
    def __init__(self, playlist):
        self.playlist = playlist
        self.index = 0

        pygame.mixer.init()
        self.load_track()

    def load_track(self):
        try:
            pygame.mixer.music.load(self.playlist[self.index])
        except pygame.error as e:
            print("ERROR loading file:", self.playlist[self.index])
            print(e)

    def play(self):
        pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.music.stop()

    def next_track(self):
        self.index = (self.index + 1) % len(self.playlist)
        self.load_track()
        pygame.mixer.music.play()

    def prev_track(self):
        self.index = (self.index - 1) % len(self.playlist)
        self.load_track()
        pygame.mixer.music.play()

    def get_current_track(self):
        return os.path.basename(self.playlist[self.index])