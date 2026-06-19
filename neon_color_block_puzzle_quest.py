import pygame
import json
import random
import os

# --- CONFIGURATION & COLORS (No White Used) ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG_COLOR = (20, 10, 30)  # Deep Purple
TEXT_COLOR = (0, 255, 255)  # Cyan
ACCENT_COLOR = (255, 0, 255) # Magenta
BLOCK_COLORS = [
    (255, 50, 50),   # Red
    (50, 255, 50),   # Green
    (50, 50, 255),   # Blue
    (255, 255, 0),   # Yellow
    (255, 100, 0)    # Orange
]

DATA_FILE = "game_data.json"

class GameState:
    def __init__(self):
        self.player_name = ""
        self.level = 1
        self.score = 0
        self.puzzle_pieces = 0
        self.music_on = True
        self.sound_on = True
        self.records = self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        return []

    def save_record(self):
        # Update or add player record
        record = {"name": self.player_name, "level": self.level, "score": self.score}
        self.records.append(record)
        # Keep only top 5 unique names
        self.records = sorted(self.records, key=lambda x: x['score'], reverse=True)[:5]
        with open(DATA_FILE, 'w') as f:
            json.dump(self.records, f)

# --- GAME ENGINE ---
class ColorBlockGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Neon Color Block: Puzzle Quest")
        self.clock = pygame.time.Clock()
        self.state = GameState()
        self.font = pygame.font.SysFont("Arial", 32)
        self.small_font = pygame.font.SysFont("Arial", 20)
        self.running = True
        self.mode = "MENU" # MENU, REGISTRATION, SETTINGS, PUZZLE, PLAYING, GAMEOVER

    def draw_text(self, text, x, y, color=TEXT_COLOR, center=True):
        surface = self.font.render(text, True, color)
        rect = surface.get_rect(center=(x, y)) if center else surface.get_rect(topleft=(x, y))
        self.screen.blit(surface, rect)

    def handle_menu(self):
        self.screen.fill(BG_COLOR)
        self.draw_text("NEON COLOR BLOCK", SCREEN_WIDTH//2, 100, ACCENT_COLOR)
        
        # Display Records
        self.draw_text("Top 5 Players:", SCREEN_WIDTH//2, 200, TEXT_COLOR)
        for i, rec in enumerate(self.state.records):
            self.draw_text(f"{rec['name']} - Lvl {rec['level']}", SCREEN_WIDTH//2, 240 + (i*30), (200, 200, 0))

        self.draw_text("Press 'S' to Start / New Player", SCREEN_WIDTH//2, 450)
        self.draw_text("Press 'O' for Settings", SCREEN_WIDTH//2, 500)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s: self.mode = "REGISTRATION"
                if event.key == pygame.K_o: self.mode = "SETTINGS"

    def handle_registration(self):
        self.screen.fill(BG_COLOR)
        self.draw_text("Enter Your Name:", SCREEN_WIDTH//2, 200)
        self.draw_text(self.state.player_name + "_", SCREEN_WIDTH//2, 250, ACCENT_COLOR)
        self.draw_text("Press ENTER to Begin", SCREEN_WIDTH//2, 350, (100, 255, 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(self.state.player_name) > 0:
                    self.mode = "PUZZLE"
                elif event.key == pygame.K_BACKSPACE:
                    self.state.player_name = self.state.player_name[:-1]
                else:
                    if len(self.state.player_name) < 10 and event.unicode.isalnum():
                        self.state.player_name += event.unicode

    def handle_puzzle_screen(self):
        self.screen.fill(BG_COLOR)
        self.draw_text(f"Puzzle Progress: {self.state.puzzle_pieces}/5", SCREEN_WIDTH//2, 50)
        
        # Draw Puzzle Grid (Mosaic)
        grid_size = 200
        start_x = (SCREEN_WIDTH - grid_size) // 2
        start_y = 150
        
        for i in range(5):
            color = BLOCK_COLORS[i] if i < self.state.puzzle_pieces else (40, 40, 40)
            pygame.draw.rect(self.screen, color, (start_x + (i*45), start_y, 40, 150))
            
        if self.state.puzzle_pieces == 5:
            self.draw_text("PUZZLE COMPLETE! YOU ARE A MASTER!", SCREEN_WIDTH//2, 400, (0, 255, 0))
            self.draw_text("Press M for Main Menu", SCREEN_WIDTH//2, 500)
        else:
            self.draw_text(f"Complete Level {self.state.level} to unlock a piece", SCREEN_WIDTH//2, 400)
            self.draw_text("Press SPACE to Play Level", SCREEN_WIDTH//2, 480, ACCENT_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.state.puzzle_pieces < 5:
                    self.mode = "PLAYING"
                if event.key == pygame.K_m: self.mode = "MENU"

    def play_level(self):
        # Simplistic Color Block Logic
        # Level 1 = 3 colors, Level 5 = 5 colors
        target_score = self.state.level * 10
        current_level_score = 0
        
        while current_level_score < target_score:
            self.screen.fill(BG_COLOR)
            self.draw_text(f"Level {self.state.level}", 100, 50)
            self.draw_text(f"Target: {current_level_score}/{target_score}", SCREEN_WIDTH - 200, 50)
            
            # Draw interactive "Blocks" (Abstracted)
            for i in range(4):
                color = BLOCK_COLORS[random.randint(0, min(self.state.level, 4))]
                pygame.draw.rect(self.screen, color, (150 + i*130, 250, 100, 100))
            
            self.draw_text("Click the Blocks rapidly to fill the meter!", SCREEN_WIDTH//2, 450, (200, 200, 200))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    current_level_score += 2
                    if self.state.sound_on: 
                        pass # Play sound logic here
                if event.type == pygame.QUIT:
                    self.running = False
                    return

        # Level Success
        self.state.puzzle_pieces += 1
        self.state.score += (self.state.level * 100)
        if self.state.level < 5:
            self.state.level += 1
        self.state.save_record()
        self.mode = "PUZZLE"

    def handle_settings(self):
        self.screen.fill(BG_COLOR)
        self.draw_text("SETTINGS", SCREEN_WIDTH//2, 100, ACCENT_COLOR)
        
        music_status = "ON" if self.state.music_on else "OFF"
        sound_status = "ON" if self.state.sound_on else "OFF"
        
        self.draw_text(f"1. Music: {music_status}", SCREEN_WIDTH//2, 250)
        self.draw_text(f"2. Sound FX: {sound_status}", SCREEN_WIDTH//2, 320)
        self.draw_text("Press 'B' to Go Back", SCREEN_WIDTH//2, 450)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: self.state.music_on = not self.state.music_on
                if event.key == pygame.K_2: self.state.sound_on = not self.state.sound_on
                if event.key == pygame.K_b: self.mode = "MENU"

    def run(self):
        while self.running:
            if self.mode == "MENU": self.handle_menu()
            elif self.mode == "REGISTRATION": self.handle_registration()
            elif self.mode == "SETTINGS": self.handle_settings()
            elif self.mode == "PUZZLE": self.handle_puzzle_screen()
            elif self.mode == "PLAYING": self.play_level()
            
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

if __name__ == "__main__":
    game = ColorBlockGame()
    game.run()

    # game finished
