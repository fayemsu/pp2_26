import os
import sys
import pygame

WIDTH = 700
HEIGHT = 250
FPS = 30


PLAYLIST = [
    "A Little Death - The Neighbourhood.mp3",
    "Mindless Self Indulgence - Bed Of Roses.mp3",
    "Mindless Self Indulgence - Unsociable.mp3",
    "Mindless Self Indulgence-Never Wanted To Dance.mp3",
    "The Neighbourhood-Devil s Advocate.mp3",
    "Земфира-главное.mp3",
    "Земфира-кто.mp3"]


class MusicPlayer:
    def __init__(self, playlist):
        self.playlist = playlist
        self.current_index = 0
        self.is_playing = False
        self.is_paused = False

    def current_track(self):
        if not self.playlist:
            return "No tracks"
        return os.path.basename(self.playlist[self.current_index])

    def load_current_track(self):
        if not self.playlist:
            return
        pygame.mixer.music.load(self.playlist[self.current_index])

    def play(self):
        if not self.playlist:
            return
        self.load_current_track()
        pygame.mixer.music.play()
        self.is_playing = True
        self.is_paused = False

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False

    def next_track(self):
        if not self.playlist:
            return
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.play()

    def previous_track(self):
        if not self.playlist:
            return
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.play()

    def get_position_seconds(self):
        pos_ms = pygame.mixer.music.get_pos()
        if pos_ms < 0:
            return 0
        return pos_ms // 1000



def format_time(seconds):
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02}:{secs:02}"


def draw_text(screen, text, font, color, x, y):
    image = font.render(text, True, color)
    screen.blit(image, (x, y))


def main():
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simple Music Player")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont(None, 32)
    small_font = pygame.font.SysFont(None, 26)

    
    
    valid_playlist = [file for file in PLAYLIST if os.path.exists(file)]

    player = MusicPlayer(valid_playlist)


    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    player.play()

                elif event.key == pygame.K_s:
                    player.stop()

                elif event.key == pygame.K_n:
                    player.next_track()

                elif event.key == pygame.K_b:
                    player.previous_track()

                elif event.key == pygame.K_q:
                    running = False

        
        if player.is_playing and not pygame.mixer.music.get_busy():
            player.next_track()

        

        screen.fill((30, 30, 40))

        draw_text(screen, "Simple Music Player", font, (255, 255, 255), 20, 20)
        draw_text(screen, f"Track: {player.current_track()}", small_font, (200, 220, 255), 20, 70)

        status = "Playing" if pygame.mixer.music.get_busy() else "Stopped"
        draw_text(screen, f"Status: {status}", small_font, (200, 255, 200), 20, 105)

        current_pos = player.get_position_seconds()
        draw_text(screen, f"Position: {format_time(current_pos)}", small_font, (255, 220, 180), 20, 140)

        draw_text(
            screen,
            "Controls: P=Play  S=Stop  N=Next  B=Back  Q=Quit",
            small_font,
            (220, 220, 220),
            20,
            190
        )

        pygame.display.flip()

    pygame.mixer.music.stop()
    pygame.quit()


if __name__ == "__main__":
    main()