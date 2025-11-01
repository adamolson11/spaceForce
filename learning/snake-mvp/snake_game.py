# snake_game.py
# Classic Snake game built with Brython (Python in the browser)

from browser import document, window, timer, bind
import random

# Game configuration
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500
GRID_SIZE = 20
INITIAL_SPEED = 150  # milliseconds per frame

# Game state
canvas = None
ctx = None
snake_body = [[200, 200], [190, 200], [180, 200]]
direction = [GRID_SIZE, 0]  # [dx, dy] - initially moving right
food_pos = [0, 0]
score = 0
game_running = False
game_paused = False
game_timer = None

def init_game():
    """Initialize the game canvas and state"""
    global canvas, ctx, snake_body, direction, food_pos, score, game_running, game_paused
    
    canvas = document["gameCanvas"]
    ctx = canvas.getContext("2d")
    
    # Reset game state
    snake_body = [[200, 200], [190, 200], [180, 200]]
    direction = [GRID_SIZE, 0]
    score = 0
    game_running = False
    game_paused = False
    
    spawn_food()
    draw_game()
    update_score_display()

def spawn_food():
    """Generate food at a random position"""
    global food_pos
    
    # Generate random position aligned to grid
    max_x = (CANVAS_WIDTH // GRID_SIZE - 1) * GRID_SIZE
    max_y = (CANVAS_HEIGHT // GRID_SIZE - 1) * GRID_SIZE
    
    food_pos = [
        random.randint(0, max_x // GRID_SIZE) * GRID_SIZE,
        random.randint(0, max_y // GRID_SIZE) * GRID_SIZE
    ]
    
    # Make sure food doesn't spawn on snake
    while food_pos in snake_body:
        food_pos = [
            random.randint(0, max_x // GRID_SIZE) * GRID_SIZE,
            random.randint(0, max_y // GRID_SIZE) * GRID_SIZE
        ]

def draw_game():
    """Draw the game state on canvas"""
    # Clear canvas
    ctx.fillStyle = "#1a1a2e"
    ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT)
    
    # Draw grid
    ctx.strokeStyle = "#16213e"
    ctx.lineWidth = 1
    for i in range(0, CANVAS_WIDTH, GRID_SIZE):
        ctx.beginPath()
        ctx.moveTo(i, 0)
        ctx.lineTo(i, CANVAS_HEIGHT)
        ctx.stroke()
    for i in range(0, CANVAS_HEIGHT, GRID_SIZE):
        ctx.beginPath()
        ctx.moveTo(0, i)
        ctx.lineTo(CANVAS_WIDTH, i)
        ctx.stroke()
    
    # Draw snake
    for i, segment in enumerate(snake_body):
        if i == 0:
            # Head is brighter
            ctx.fillStyle = "#4ecca3"
        else:
            ctx.fillStyle = "#3ea78a"
        ctx.fillRect(segment[0], segment[1], GRID_SIZE - 2, GRID_SIZE - 2)
    
    # Draw food
    ctx.fillStyle = "#ff6b6b"
    ctx.fillRect(food_pos[0], food_pos[1], GRID_SIZE - 2, GRID_SIZE - 2)

def move_snake():
    """Update snake position"""
    global snake_body, score, game_running
    
    if not game_running or game_paused:
        return
    
    # Calculate new head position
    head = snake_body[0]
    new_head = [head[0] + direction[0], head[1] + direction[1]]
    
    # Check collision with walls
    if (new_head[0] < 0 or new_head[0] >= CANVAS_WIDTH or
        new_head[1] < 0 or new_head[1] >= CANVAS_HEIGHT):
        game_over()
        return
    
    # Check collision with self
    if new_head in snake_body:
        game_over()
        return
    
    # Add new head
    snake_body.insert(0, new_head)
    
    # Check if food eaten
    if new_head[0] == food_pos[0] and new_head[1] == food_pos[1]:
        score += 10
        update_score_display()
        spawn_food()
        # Don't remove tail - snake grows
    else:
        # Remove tail - snake moves without growing
        snake_body.pop()
    
    draw_game()

def game_loop():
    """Main game loop"""
    move_snake()

def start_game():
    """Start the game"""
    global game_running, game_timer
    
    if not game_running:
        game_running = True
        game_paused = False
        document["startBtn"].textContent = "Pause"
        game_timer = timer.set_interval(game_loop, INITIAL_SPEED)
    elif game_paused:
        game_paused = False
        document["startBtn"].textContent = "Pause"
        game_timer = timer.set_interval(game_loop, INITIAL_SPEED)

def pause_game():
    """Pause the game"""
    global game_paused, game_timer
    
    if game_running and not game_paused:
        game_paused = True
        if game_timer is not None:
            timer.clear_interval(game_timer)
        document["startBtn"].textContent = "Resume"

def restart_game():
    """Restart the game"""
    global game_timer, game_running, game_paused
    
    # Stop current game
    if game_timer is not None:
        timer.clear_interval(game_timer)
    
    game_running = False
    game_paused = False
    
    # Reset and start new game
    init_game()
    document["startBtn"].textContent = "Start"

def game_over():
    """Handle game over"""
    global game_running, game_timer
    
    game_running = False
    
    if game_timer is not None:
        timer.clear_interval(game_timer)
    
    # Draw game over message
    ctx.fillStyle = "rgba(0, 0, 0, 0.7)"
    ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT)
    
    ctx.fillStyle = "#ffffff"
    ctx.font = "40px Arial"
    ctx.textAlign = "center"
    ctx.fillText("Game Over!", CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2 - 20)
    ctx.font = "20px Arial"
    ctx.fillText(f"Score: {score}", CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2 + 20)
    ctx.fillText("Click Restart to play again", CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2 + 50)
    
    document["startBtn"].textContent = "Start"

def update_score_display():
    """Update the score display"""
    document["scoreDisplay"].textContent = f"Score: {score}"

@bind(document, "keydown")
def on_keydown(event):
    """Handle keyboard input for snake direction"""
    global direction
    
    if not game_running:
        return
    
    # Prevent snake from going backward
    if event.key == "ArrowUp" and direction[1] != GRID_SIZE:
        direction = [0, -GRID_SIZE]
        event.preventDefault()
    elif event.key == "ArrowDown" and direction[1] != -GRID_SIZE:
        direction = [0, GRID_SIZE]
        event.preventDefault()
    elif event.key == "ArrowLeft" and direction[0] != GRID_SIZE:
        direction = [-GRID_SIZE, 0]
        event.preventDefault()
    elif event.key == "ArrowRight" and direction[0] != -GRID_SIZE:
        direction = [GRID_SIZE, 0]
        event.preventDefault()

# Button event handlers
def on_start_click(event):
    """Handle start/pause button click"""
    if not game_running or game_paused:
        start_game()
    else:
        pause_game()

def on_restart_click(event):
    """Handle restart button click"""
    restart_game()

# Initialize game when script loads
init_game()

# Bind button events
document["startBtn"].bind("click", on_start_click)
document["restartBtn"].bind("click", on_restart_click)
