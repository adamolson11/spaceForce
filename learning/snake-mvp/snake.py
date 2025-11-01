from browser import document, window, timer, html
import random

# Game constants
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400
GRID_SIZE = 20
GRID_WIDTH = CANVAS_WIDTH // GRID_SIZE
GRID_HEIGHT = CANVAS_HEIGHT // GRID_SIZE
GAME_SPEED = 150  # milliseconds between game updates

# Game state
class SnakeGame:
    def __init__(self):
        self.canvas = document["gameCanvas"]
        self.ctx = self.canvas.getContext("2d")
        self.reset()
        self.running = False
        self.game_loop_timer = None
        
    def reset(self):
        """Reset the game to initial state"""
        self.snake = [[5, 5], [4, 5], [3, 5]]  # Start with 3 segments
        self.direction = [1, 0]  # Moving right
        self.next_direction = [1, 0]  # Buffer for next direction
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
        
    def generate_food(self):
        """Generate food at a random position not occupied by snake"""
        while True:
            food = [
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1)
            ]
            if food not in self.snake:
                return food
    
    def move(self):
        """Move the snake one step"""
        if self.game_over:
            return
            
        # Update direction from buffer
        self.direction = self.next_direction[:]
        
        # Calculate new head position
        head = self.snake[0][:]
        head[0] += self.direction[0]
        head[1] += self.direction[1]
        
        # Check wall collision
        if (head[0] < 0 or head[0] >= GRID_WIDTH or 
            head[1] < 0 or head[1] >= GRID_HEIGHT):
            self.game_over = True
            self.running = False
            window.alert(f"Game Over! Your score: {self.score}")
            return
        
        # Check self collision
        if head in self.snake:
            self.game_over = True
            self.running = False
            window.alert(f"Game Over! You hit yourself. Score: {self.score}")
            return
        
        # Add new head
        self.snake.insert(0, head)
        
        # Check if food is eaten
        if head == self.food:
            self.score += 10
            self.food = self.generate_food()
            document["scoreDisplay"].textContent = str(self.score)
        else:
            # Remove tail if no food eaten
            self.snake.pop()
    
    def change_direction(self, new_direction):
        """Change snake direction (prevent 180-degree turns)"""
        # Can't reverse direction
        if (new_direction[0] != -self.direction[0] and 
            new_direction[1] != -self.direction[1]):
            self.next_direction = new_direction
    
    def draw(self):
        """Draw the game state"""
        # Clear canvas
        self.ctx.fillStyle = "#1a1a2e"
        self.ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT)
        
        # Draw grid lines (optional, subtle)
        self.ctx.strokeStyle = "#16213e"
        self.ctx.lineWidth = 1
        for i in range(0, CANVAS_WIDTH, GRID_SIZE):
            self.ctx.beginPath()
            self.ctx.moveTo(i, 0)
            self.ctx.lineTo(i, CANVAS_HEIGHT)
            self.ctx.stroke()
        for i in range(0, CANVAS_HEIGHT, GRID_SIZE):
            self.ctx.beginPath()
            self.ctx.moveTo(0, i)
            self.ctx.lineTo(CANVAS_WIDTH, i)
            self.ctx.stroke()
        
        # Draw snake
        for i, segment in enumerate(self.snake):
            if i == 0:
                # Head is brighter
                self.ctx.fillStyle = "#00ff00"
            else:
                # Body segments
                self.ctx.fillStyle = "#00cc00"
            
            self.ctx.fillRect(
                segment[0] * GRID_SIZE + 1,
                segment[1] * GRID_SIZE + 1,
                GRID_SIZE - 2,
                GRID_SIZE - 2
            )
        
        # Draw food
        self.ctx.fillStyle = "#ff0000"
        self.ctx.fillRect(
            self.food[0] * GRID_SIZE + 1,
            self.food[1] * GRID_SIZE + 1,
            GRID_SIZE - 2,
            GRID_SIZE - 2
        )
        
        # Draw score on canvas
        self.ctx.fillStyle = "#ffffff"
        self.ctx.font = "16px Arial"
        self.ctx.fillText(f"Score: {self.score}", 10, 20)
    
    def game_loop(self):
        """Main game loop"""
        if self.running:
            self.move()
            self.draw()
    
    def start(self):
        """Start the game"""
        if not self.running:
            self.running = True
            if self.game_over:
                self.reset()
                self.game_over = False
            # Start the game loop
            self.game_loop_timer = timer.set_interval(self.game_loop, GAME_SPEED)
    
    def pause(self):
        """Pause the game"""
        self.running = False
        if self.game_loop_timer is not None:
            timer.clear_interval(self.game_loop_timer)
            self.game_loop_timer = None
    
    def restart(self):
        """Restart the game"""
        self.pause()
        self.reset()
        self.draw()

# Create game instance
game = SnakeGame()

# Initial draw
game.draw()

# Keyboard controls
def on_keydown(event):
    key = event.key
    if key == "ArrowUp" or key == "w" or key == "W":
        game.change_direction([0, -1])
        event.preventDefault()
    elif key == "ArrowDown" or key == "s" or key == "S":
        game.change_direction([0, 1])
        event.preventDefault()
    elif key == "ArrowLeft" or key == "a" or key == "A":
        game.change_direction([-1, 0])
        event.preventDefault()
    elif key == "ArrowRight" or key == "d" or key == "D":
        game.change_direction([1, 0])
        event.preventDefault()

document.bind("keydown", on_keydown)

# Button controls
def start_game(event):
    game.start()
    document["startBtn"].textContent = "Start"

def pause_game(event):
    game.pause()

def restart_game(event):
    game.restart()

document["startBtn"].bind("click", start_game)
document["pauseBtn"].bind("click", pause_game)
document["restartBtn"].bind("click", restart_game)
