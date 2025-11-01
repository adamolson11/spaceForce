"""
Snake Game with Quiz Integration - A Pygame-based Snake game that shows quizzes
every few minutes and includes an in-game store.
"""
import pygame
import random
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from quiz.quiz_manager import QuizManager
from store import Store


# Game Configuration
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GAME_SPEED = 10  # FPS

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)

# Quiz Configuration
QUIZ_INTERVAL_SECONDS = 180  # 3 minutes - Change to 20 for quick demo
DEMO_MODE = False  # Set to True to show first quiz after 10 seconds


class SnakeGame:
    """Main Snake Game class with quiz and store integration."""
    
    def __init__(self):
        """Initialize the game."""
        pygame.init()
        
        # Setup display
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game with Quiz")
        self.clock = pygame.time.Clock()
        
        # Setup fonts
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Game state
        self.reset_game()
        
        # Coins (earned from eating apples and quizzes)
        self.coins = 0
        
        # Quiz manager
        questions_file = os.path.join(os.path.dirname(__file__), 'quiz', 'questions.json')
        self.quiz_manager = QuizManager(
            questions_file=questions_file,
            quiz_interval=QUIZ_INTERVAL_SECONDS,
            pause_callback=self.pause_for_quiz,
            resume_callback=self.resume_from_quiz,
            on_answer_callback=self.on_quiz_answer,
            server_url=None,  # Set to your Google Apps Script URL if you deployed it
            demo_mode=DEMO_MODE
        )
        
        # Store
        self.store = Store()
        self.show_store = False
        
        # Game states
        self.running = True
        self.paused = False
        self.game_over = False
    
    def reset_game(self):
        """Reset game state for new game."""
        # Snake starts in the middle, moving right
        start_x = WINDOW_WIDTH // 2
        start_y = WINDOW_HEIGHT // 2
        self.snake = [
            [start_x, start_y],
            [start_x - GRID_SIZE, start_y],
            [start_x - 2 * GRID_SIZE, start_y]
        ]
        self.direction = [GRID_SIZE, 0]
        self.next_direction = [GRID_SIZE, 0]
        
        # Spawn first apple
        self.apple = self.spawn_apple()
        
        # Score
        self.score = 0
    
    def spawn_apple(self):
        """Spawn apple at random location not on snake."""
        while True:
            x = random.randint(0, (WINDOW_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
            y = random.randint(0, (WINDOW_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
            
            if [x, y] not in self.snake:
                return [x, y]
    
    def pause_for_quiz(self):
        """Callback to pause game when quiz starts."""
        self.paused = True
    
    def resume_from_quiz(self):
        """Callback to resume game after quiz ends."""
        self.paused = False
    
    def on_quiz_answer(self, correct: bool, coins: int):
        """Callback when quiz answer is submitted."""
        self.coins += coins
        if correct:
            print(f"Correct! +{coins} coins. Total: {self.coins}")
        else:
            print(f"Wrong answer. Total coins: {self.coins}")
    
    def handle_input(self):
        """Handle keyboard and event input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                # Handle quiz answer selection
                if self.quiz_manager.quiz_active:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                        choice = event.key - pygame.K_1  # Convert to 0-3
                        self.quiz_manager.submit_answer(choice)
                    continue
                
                # Handle store toggle
                if event.key == pygame.K_s and not self.paused:
                    self.show_store = not self.show_store
                    continue
                
                # Handle store purchase
                if self.show_store and event.key == pygame.K_p:
                    if self.coins >= 20:
                        self.coins -= 20
                        prize = self.store.purchase_item()
                        print(f"Purchased: {prize}! Remaining coins: {self.coins}")
                    else:
                        print("Not enough coins! Need 20 coins.")
                    continue
                
                # Handle snake direction
                if not self.paused and not self.game_over:
                    if event.key == pygame.K_UP and self.direction[1] != GRID_SIZE:
                        self.next_direction = [0, -GRID_SIZE]
                    elif event.key == pygame.K_DOWN and self.direction[1] != -GRID_SIZE:
                        self.next_direction = [0, GRID_SIZE]
                    elif event.key == pygame.K_LEFT and self.direction[0] != GRID_SIZE:
                        self.next_direction = [-GRID_SIZE, 0]
                    elif event.key == pygame.K_RIGHT and self.direction[0] != -GRID_SIZE:
                        self.next_direction = [GRID_SIZE, 0]
                
                # Handle restart
                if event.key == pygame.K_r and self.game_over:
                    self.reset_game()
                    self.game_over = False
    
    def update(self):
        """Update game state."""
        if self.paused or self.game_over:
            return
        
        # Check for quiz time
        self.quiz_manager.check_and_show_quiz()
        
        if self.quiz_manager.quiz_active:
            return
        
        # Update direction
        self.direction = self.next_direction
        
        # Move snake
        head = self.snake[0].copy()
        head[0] += self.direction[0]
        head[1] += self.direction[1]
        
        # Check wall collision
        if (head[0] < 0 or head[0] >= WINDOW_WIDTH or
            head[1] < 0 or head[1] >= WINDOW_HEIGHT):
            self.game_over = True
            return
        
        # Check self collision
        if head in self.snake:
            self.game_over = True
            return
        
        # Add new head
        self.snake.insert(0, head)
        
        # Check apple collision
        if head == self.apple:
            self.score += 1
            self.coins += 1  # 1 coin per apple
            self.apple = self.spawn_apple()
        else:
            # Remove tail if no apple eaten
            self.snake.pop()
    
    def draw(self):
        """Draw everything on screen."""
        # Clear screen
        self.screen.fill(BLACK)
        
        # Draw quiz if active
        if self.quiz_manager.quiz_active:
            self.draw_quiz()
            return
        
        # Draw store if active
        if self.show_store:
            self.draw_store()
            return
        
        # Draw snake
        for segment in self.snake:
            pygame.draw.rect(self.screen, GREEN, (*segment, GRID_SIZE, GRID_SIZE))
        
        # Draw apple
        pygame.draw.rect(self.screen, RED, (*self.apple, GRID_SIZE, GRID_SIZE))
        
        # Draw HUD
        self.draw_hud()
        
        # Draw game over
        if self.game_over:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def draw_hud(self):
        """Draw heads-up display (score, coins, etc.)."""
        # Score
        score_text = self.small_font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Coins
        coins_text = self.small_font.render(f"Coins: {self.coins}", True, YELLOW)
        self.screen.blit(coins_text, (10, 40))
        
        # Inventory count
        inv_count = self.store.get_inventory_count()
        inv_text = self.small_font.render(f"Items: {inv_count}", True, BLUE)
        self.screen.blit(inv_text, (10, 70))
        
        # Instructions
        help_text = self.small_font.render("Press S for Store", True, GRAY)
        self.screen.blit(help_text, (WINDOW_WIDTH - 200, 10))
    
    def draw_quiz(self):
        """Draw quiz overlay."""
        question = self.quiz_manager.get_current_question()
        if not question:
            return
        
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(230)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Quiz title
        title = self.font.render("QUIZ TIME!", True, YELLOW)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        # Question
        question_lines = self.wrap_text(question['question'], 700)
        y_offset = 160
        for line in question_lines:
            q_text = self.small_font.render(line, True, WHITE)
            q_rect = q_text.get_rect(center=(WINDOW_WIDTH // 2, y_offset))
            self.screen.blit(q_text, q_rect)
            y_offset += 30
        
        # Choices
        y_offset += 20
        for i, choice in enumerate(question['choices']):
            choice_text = self.small_font.render(f"{i+1}. {choice}", True, WHITE)
            choice_rect = choice_text.get_rect(center=(WINDOW_WIDTH // 2, y_offset))
            self.screen.blit(choice_text, choice_rect)
            y_offset += 40
        
        # Instructions
        inst_text = self.small_font.render("Press 1-4 to answer", True, GRAY)
        inst_rect = inst_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50))
        self.screen.blit(inst_text, inst_rect)
    
    def draw_store(self):
        """Draw store overlay."""
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(230)
        overlay.fill(DARK_GRAY)
        self.screen.blit(overlay, (0, 0))
        
        # Store title
        title = self.font.render("STORE", True, YELLOW)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 80))
        self.screen.blit(title, title_rect)
        
        # Your coins
        coins_text = self.small_font.render(f"Your Coins: {self.coins}", True, WHITE)
        coins_rect = coins_text.get_rect(center=(WINDOW_WIDTH // 2, 140))
        self.screen.blit(coins_text, coins_rect)
        
        # Purchase option
        purchase_text = self.small_font.render("Random Prize: 20 coins", True, WHITE)
        purchase_rect = purchase_text.get_rect(center=(WINDOW_WIDTH // 2, 200))
        self.screen.blit(purchase_text, purchase_rect)
        
        buy_text = self.small_font.render("Press P to Purchase", True, GREEN if self.coins >= 20 else RED)
        buy_rect = buy_text.get_rect(center=(WINDOW_WIDTH // 2, 240))
        self.screen.blit(buy_text, buy_rect)
        
        # Inventory
        inv_title = self.small_font.render("Your Inventory:", True, WHITE)
        inv_title_rect = inv_title.get_rect(center=(WINDOW_WIDTH // 2, 300))
        self.screen.blit(inv_title, inv_title_rect)
        
        inventory = self.store.get_inventory_summary()
        if inventory:
            y_offset = 340
            for item, count in sorted(inventory.items()):
                item_text = self.small_font.render(f"{item} x{count}", True, WHITE)
                item_rect = item_text.get_rect(center=(WINDOW_WIDTH // 2, y_offset))
                self.screen.blit(item_text, item_rect)
                y_offset += 30
                if y_offset > WINDOW_HEIGHT - 100:
                    break
        else:
            empty_text = self.small_font.render("(empty)", True, GRAY)
            empty_rect = empty_text.get_rect(center=(WINDOW_WIDTH // 2, 340))
            self.screen.blit(empty_text, empty_rect)
        
        # Close instructions
        close_text = self.small_font.render("Press S to close", True, GRAY)
        close_rect = close_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40))
        self.screen.blit(close_text, close_rect)
    
    def draw_game_over(self):
        """Draw game over overlay."""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game Over text
        game_over_text = self.font.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Score
        score_text = self.small_font.render(f"Final Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)
        
        # Coins
        coins_text = self.small_font.render(f"Total Coins: {self.coins}", True, YELLOW)
        coins_rect = coins_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40))
        self.screen.blit(coins_text, coins_rect)
        
        # Restart
        restart_text = self.small_font.render("Press R to Restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80))
        self.screen.blit(restart_text, restart_rect)
    
    def wrap_text(self, text: str, max_width: int):
        """Wrap text to fit within max_width."""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if self.small_font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(GAME_SPEED)
        
        # Show stats before quitting
        stats = self.quiz_manager.get_quiz_stats()
        print("\n" + "="*50)
        print("Game Statistics:")
        print(f"Final Score: {self.score}")
        print(f"Total Coins: {self.coins}")
        print(f"Quizzes Taken: {stats['total_quizzes']}")
        print(f"Correct Answers: {stats['correct_answers']}")
        print(f"Accuracy: {stats['accuracy']:.1f}%")
        print(f"Quiz Coins Earned: {stats['total_coins']}")
        print(f"Items Purchased: {self.store.get_inventory_count()}")
        print("="*50)
        
        pygame.quit()
        sys.exit()


def main():
    """Entry point for the game."""
    game = SnakeGame()
    game.run()


if __name__ == "__main__":
    main()
