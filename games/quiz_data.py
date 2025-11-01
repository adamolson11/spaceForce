# Quiz questions for the Snake Game MVP
# Each question has: question text, options, correct answer index, and explanation

quiz_questions = [
    {
        "question": "What data structure is best for storing the snake's body segments?",
        "options": [
            "A string",
            "A list/array",
            "A dictionary",
            "A single variable"
        ],
        "correct": 1,
        "explanation": "A list/array is perfect because the snake is made of multiple segments that need to be tracked in order."
    },
    {
        "question": "In the Snake game, what happens when the snake eats food?",
        "options": [
            "The snake gets shorter",
            "The game ends",
            "The snake grows longer",
            "Nothing happens"
        ],
        "correct": 2,
        "explanation": "When the snake eats food, it grows longer by one segment, making the game progressively harder."
    },
    {
        "question": "What Python data type would you use to store the snake's direction?",
        "options": [
            "A boolean (True/False)",
            "A list of two numbers [x, y]",
            "A single number",
            "A string like 'hello'"
        ],
        "correct": 1,
        "explanation": "Direction needs both x and y components, so a list of two numbers like [1, 0] for right or [0, 1] for down works perfectly."
    },
    {
        "question": "What does a game loop do?",
        "options": [
            "It runs the game code once and stops",
            "It repeatedly updates and draws the game",
            "It saves the game progress",
            "It loads images from files"
        ],
        "correct": 1,
        "explanation": "A game loop continuously updates the game state (like moving the snake) and redraws the screen to create animation."
    },
    {
        "question": "How do you check if the snake hits the wall?",
        "options": [
            "Ask the player if they hit the wall",
            "Compare the snake's position with the game boundaries",
            "Wait for an error to occur",
            "Use a random number generator"
        ],
        "correct": 1,
        "explanation": "We compare the snake head's x,y coordinates with the game boundaries (0 and width/height) to detect collisions."
    },
    {
        "question": "What is a 'collision' in game programming?",
        "options": [
            "When the computer crashes",
            "When two game objects touch or overlap",
            "When you click the mouse",
            "When the game loads"
        ],
        "correct": 1,
        "explanation": "Collision detection checks if two game objects (like the snake and food, or snake and wall) are touching or overlapping."
    }
]
