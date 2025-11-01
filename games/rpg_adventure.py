from browser import document, window, timer, html
import random

# Game constants
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
GRID_SIZE = 40  # Size of each grid cell
GRID_WIDTH = CANVAS_WIDTH // GRID_SIZE
GRID_HEIGHT = CANVAS_HEIGHT // GRID_SIZE

# Colors
COLOR_GRID = "#1a1a2e"
COLOR_GRID_LINES = "#2a2a3e"
COLOR_PLAYER = "#00ff00"
COLOR_GRASS = "#2d5016"
COLOR_PATH = "#5a4a3a"

# Game state
class RPGGame:
    def __init__(self):
        self.canvas = document["gameCanvas"]
        self.ctx = self.canvas.getContext("2d")
        self.reset()
        self.running = False
        self.keys_pressed = set()
        self.last_update = 0
        self.move_cooldown = 150  # milliseconds between moves
        
    def reset(self):
        """Reset the game to initial state"""
        # Player starts in the center of the grid
        self.player_x = GRID_WIDTH // 2
        self.player_y = GRID_HEIGHT // 2
        self.steps = 0
        self.game_over = False
        
        # Generate a simple terrain
        self.terrain = self.generate_terrain()
        
    def generate_terrain(self):
        """Generate simple terrain (grass with some paths)"""
        terrain = []
        for y in range(GRID_HEIGHT):
            row = []
            for x in range(GRID_WIDTH):
                # Create a simple cross-path pattern
                if x == GRID_WIDTH // 2 or y == GRID_HEIGHT // 2:
                    row.append('path')
                else:
                    row.append('grass')
            terrain.append(row)
        return terrain
    
    def draw_grid(self):
        """Draw the grid background"""
        # Draw terrain
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                # Draw terrain tile
                if self.terrain[y][x] == 'path':
                    self.ctx.fillStyle = COLOR_PATH
                else:
                    self.ctx.fillStyle = COLOR_GRASS
                
                self.ctx.fillRect(
                    x * GRID_SIZE,
                    y * GRID_SIZE,
                    GRID_SIZE,
                    GRID_SIZE
                )
        
        # Draw grid lines
        self.ctx.strokeStyle = COLOR_GRID_LINES
        self.ctx.lineWidth = 1
        
        # Vertical lines
        for x in range(GRID_WIDTH + 1):
            self.ctx.beginPath()
            self.ctx.moveTo(x * GRID_SIZE, 0)
            self.ctx.lineTo(x * GRID_SIZE, CANVAS_HEIGHT)
            self.ctx.stroke()
        
        # Horizontal lines
        for y in range(GRID_HEIGHT + 1):
            self.ctx.beginPath()
            self.ctx.moveTo(0, y * GRID_SIZE)
            self.ctx.lineTo(CANVAS_WIDTH, y * GRID_SIZE)
            self.ctx.stroke()
    
    def draw_player(self):
        """Draw the player avatar"""
        # Draw a simple hero representation
        # Body (circle)
        self.ctx.fillStyle = COLOR_PLAYER
        center_x = self.player_x * GRID_SIZE + GRID_SIZE // 2
        center_y = self.player_y * GRID_SIZE + GRID_SIZE // 2
        
        # Draw hero as a circle with a border
        self.ctx.beginPath()
        self.ctx.arc(center_x, center_y, GRID_SIZE // 3, 0, 2 * 3.14159)
        self.ctx.fill()
        
        # Add a border
        self.ctx.strokeStyle = "#00cc00"
        self.ctx.lineWidth = 2
        self.ctx.stroke()
        
        # Draw a simple face
        # Eyes
        self.ctx.fillStyle = "#000000"
        self.ctx.beginPath()
        self.ctx.arc(center_x - 5, center_y - 3, 2, 0, 2 * 3.14159)
        self.ctx.fill()
        self.ctx.beginPath()
        self.ctx.arc(center_x + 5, center_y - 3, 2, 0, 2 * 3.14159)
        self.ctx.fill()
        
        # Smile
        self.ctx.strokeStyle = "#000000"
        self.ctx.lineWidth = 2
        self.ctx.beginPath()
        self.ctx.arc(center_x, center_y + 2, 6, 0, 3.14159)
        self.ctx.stroke()
    
    def draw(self):
        """Draw the game state"""
        # Clear canvas
        self.ctx.fillStyle = COLOR_GRID
        self.ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT)
        
        # Draw grid and terrain
        self.draw_grid()
        
        # Draw player
        self.draw_player()
        
        # Update UI
        document["stepsDisplay"].textContent = str(self.steps)
        document["positionDisplay"].textContent = f"{self.player_x}, {self.player_y}"
    
    def move_player(self, dx, dy):
        """Move player by dx, dy if valid"""
        new_x = self.player_x + dx
        new_y = self.player_y + dy
        
        # Check boundaries
        if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
            self.player_x = new_x
            self.player_y = new_y
            self.steps += 1
            return True
        return False
    
    def update(self):
        """Update game state based on input"""
        if not self.running:
            return
        
        current_time = window.performance.now()
        if current_time - self.last_update < self.move_cooldown:
            return
        
        moved = False
        
        # Check which keys are pressed and move accordingly
        if 'ArrowUp' in self.keys_pressed or 'w' in self.keys_pressed or 'W' in self.keys_pressed:
            moved = self.move_player(0, -1)
        elif 'ArrowDown' in self.keys_pressed or 's' in self.keys_pressed or 'S' in self.keys_pressed:
            moved = self.move_player(0, 1)
        elif 'ArrowLeft' in self.keys_pressed or 'a' in self.keys_pressed or 'A' in self.keys_pressed:
            moved = self.move_player(-1, 0)
        elif 'ArrowRight' in self.keys_pressed or 'd' in self.keys_pressed or 'D' in self.keys_pressed:
            moved = self.move_player(1, 0)
        
        if moved:
            self.last_update = current_time
            self.draw()
    
    def game_loop(self):
        """Main game loop"""
        if self.running:
            self.update()
    
    def start(self):
        """Start the game"""
        if not self.running:
            self.running = True
            if self.game_over:
                self.reset()
                self.game_over = False
            self.draw()
    
    def pause(self):
        """Pause the game"""
        self.running = False
    
    def restart(self):
        """Restart the game"""
        self.pause()
        self.reset()
        self.draw()

# Create game instance
game = RPGGame()

# Initial draw
game.draw()

# Keyboard controls
def on_keydown(event):
    key = event.key
    game.keys_pressed.add(key)
    event.preventDefault()

def on_keyup(event):
    key = event.key
    if key in game.keys_pressed:
        game.keys_pressed.remove(key)

document.bind("keydown", on_keydown)
document.bind("keyup", on_keyup)

# Button controls
def start_game(event):
    game.start()
    document["startBtn"].textContent = "Playing..."

def pause_game(event):
    game.pause()
    document["startBtn"].textContent = "Resume"

def restart_game(event):
    game.restart()
    document["startBtn"].textContent = "Start Adventure"

document["startBtn"].bind("click", start_game)
document["pauseBtn"].bind("click", pause_game)
document["restartBtn"].bind("click", restart_game)

# Set up game loop
timer.set_interval(game.game_loop, 16)  # ~60 FPS
