# quiz_data.py
# Quiz questions about the Snake game and Python programming

quiz_questions = [
    {
        "id": 1,
        "question": "What data structure is best for storing the snake's body segments?",
        "choices": [
            "A list (array) of coordinates",
            "A single variable",
            "A dictionary",
            "A string"
        ],
        "correct": 0,
        "explanation": "A list allows us to store multiple coordinate pairs and easily add/remove segments as the snake grows or moves.",
        "code_reference": "snake_body"
    },
    {
        "id": 2,
        "question": "How do we make the snake move continuously?",
        "choices": [
            "Call a function once",
            "Use a timer/interval to repeatedly update position",
            "Wait for user input each time",
            "Use a while loop"
        ],
        "correct": 1,
        "explanation": "We use setInterval() or requestAnimationFrame() to repeatedly call the game update function, creating smooth continuous movement.",
        "code_reference": "game_loop"
    },
    {
        "id": 3,
        "question": "What happens when the snake eats food?",
        "choices": [
            "The game ends",
            "The snake gets faster",
            "A new segment is added to the snake's body",
            "Nothing happens"
        ],
        "correct": 2,
        "explanation": "When the snake's head reaches food coordinates, we add a new segment to the body list and generate new food at a random location.",
        "code_reference": "collision_detection"
    },
    {
        "id": 4,
        "question": "How do we detect if the snake hits the wall?",
        "choices": [
            "Check if head coordinates are outside the canvas boundaries",
            "Wait for an error message",
            "The browser detects it automatically",
            "Count the number of moves"
        ],
        "correct": 0,
        "explanation": "We check if the snake's head x/y coordinates are less than 0 or greater than the canvas width/height.",
        "code_reference": "collision_detection"
    },
    {
        "id": 5,
        "question": "What Python concept allows us to group related game data together?",
        "choices": [
            "Variables",
            "Classes/Objects",
            "Comments",
            "Print statements"
        ],
        "correct": 1,
        "explanation": "Classes let us create objects that bundle data (snake position, direction, score) and methods (move, grow, check_collision) together.",
        "code_reference": "snake_class"
    },
    {
        "id": 6,
        "question": "How do we change the snake's direction when arrow keys are pressed?",
        "choices": [
            "Automatically happens",
            "Listen for keyboard events and update direction variables",
            "Use the mouse",
            "Type commands in the console"
        ],
        "correct": 1,
        "explanation": "We add event listeners for keydown events, check which arrow key was pressed, and update the snake's direction (dx, dy) accordingly.",
        "code_reference": "input_handling"
    }
]

# Code snippets that map to quiz questions
code_snippets = {
    "snake_body": """# Storing snake body as a list of [x, y] coordinates
snake_body = [
    [200, 200],  # Head
    [190, 200],  # Body segment 1
    [180, 200]   # Body segment 2
]""",
    
    "game_loop": """# Game loop using timer
def game_loop():
    move_snake()
    check_collisions()
    draw_game()
    
# Call game_loop repeatedly (every 100ms)
timer.set_interval(game_loop, 100)""",
    
    "collision_detection": """# Check if snake eats food
if snake_head[0] == food_x and snake_head[1] == food_y:
    score += 1
    # Add new segment (snake grows)
    snake_body.append([food_x, food_y])
    spawn_new_food()

# Check if snake hits wall
if (snake_head[0] < 0 or snake_head[0] >= canvas_width or
    snake_head[1] < 0 or snake_head[1] >= canvas_height):
    game_over()""",
    
    "snake_class": """# Using a class to organize game data
class Snake:
    def __init__(self):
        self.body = [[200, 200]]
        self.direction = [10, 0]
        self.score = 0
    
    def move(self):
        head = self.body[0]
        new_head = [
            head[0] + self.direction[0],
            head[1] + self.direction[1]
        ]
        self.body.insert(0, new_head)
        self.body.pop()
    
    def grow(self):
        self.body.append(self.body[-1])""",
    
    "input_handling": """# Handle keyboard input
from browser import document, bind

@bind(document, "keydown")
def on_keydown(event):
    if event.key == "ArrowUp" and direction[1] != grid_size:
        direction[0] = 0
        direction[1] = -grid_size
    elif event.key == "ArrowDown" and direction[1] != -grid_size:
        direction[0] = 0
        direction[1] = grid_size
    elif event.key == "ArrowLeft" and direction[0] != grid_size:
        direction[0] = -grid_size
        direction[1] = 0
    elif event.key == "ArrowRight" and direction[0] != -grid_size:
        direction[0] = grid_size
        direction[1] = 0"""
}
