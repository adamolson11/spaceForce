# Snake Game with Quiz Integration

A Pygame-based Snake game that demonstrates educational game mechanics with auto-quiz functionality, an in-game store, and optional backend data collection via Google Apps Script.

## Features

- **Classic Snake Gameplay**: Control the snake with arrow keys, eat apples to grow
- **Coin System**: Earn 1 coin per apple eaten
- **Auto-Quiz Every 3 Minutes**: Game pauses automatically to show a quiz question
- **Quiz Rewards**: Earn 10 coins for each correct answer
- **In-Game Store**: Spend 20 coins on random prizes (press S to open)
- **Persistent Progress**: Quiz results and inventory saved locally
- **Optional Backend**: Can POST quiz results to Google Apps Script for teacher dashboards

## Quick Start

### Installation

1. **Install Python 3.8 or higher** (if not already installed)

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game**:
   ```bash
   python src/snake_game.py
   ```

### Controls

- **Arrow Keys**: Move the snake (Up, Down, Left, Right)
- **S**: Open/close the store
- **P**: Purchase item in store (costs 20 coins)
- **1-4**: Answer quiz questions (when quiz appears)
- **R**: Restart game (after game over)

## Demo Mode

To test the quiz feature quickly without waiting 3 minutes:

1. Open `src/snake_game.py`
2. Find the line: `QUIZ_INTERVAL_SECONDS = 180`
3. Change it to: `QUIZ_INTERVAL_SECONDS = 20` (quiz every 20 seconds)
4. Or set `DEMO_MODE = True` to show the first quiz after just 10 seconds

## File Structure

```
spaceForce/
├── src/
│   ├── snake_game.py           # Main game file
│   ├── store.py                # In-game store logic
│   └── quiz/
│       ├── quiz_manager.py     # Quiz timing and logic
│       └── questions.json      # Quiz questions database
├── server/
│   └── google_apps_script.gs   # Google Apps Script for backend
├── requirements.txt            # Python dependencies
└── README_SNAKE.md            # This file
```

## How It Works

### Game Loop
1. Snake moves continuously in the current direction
2. Player collects apples to grow and earn coins
3. Every 3 minutes (configurable), the game pauses for a quiz
4. Player can open store anytime to spend coins on prizes

### Quiz System
- **QuizManager** tracks time and shows quizzes at intervals
- Questions loaded from `src/quiz/questions.json`
- Pauses game via callback when quiz starts
- Awards coins for correct answers
- Saves results to `quiz_results.json`
- Optionally POSTs results to server

### Store System
- Players can buy random prizes for 20 coins each
- Inventory persisted to `store_state.json`
- 10 different prize types available
- View inventory summary in store screen

## Google Apps Script Backend (Optional)

The game can POST quiz results to a Google Sheets backend for teacher monitoring.

### Setup Instructions

1. **Create a new Google Sheet**

2. **Open Script Editor**:
   - In Google Sheets: Extensions → Apps Script

3. **Copy the script**:
   - Copy contents of `server/google_apps_script.gs`
   - Paste into the Apps Script editor

4. **Configure SECRET_TOKEN**:
   - Change `YOUR_SECRET_TOKEN_HERE` to a random string

5. **Deploy as Web App**:
   - Click "Deploy" → "New deployment"
   - Select type: "Web app"
   - Execute as: "Me"
   - Who has access: "Anyone"
   - Click "Deploy"
   - Copy the web app URL

6. **Update game code**:
   - Open `src/snake_game.py`
   - Find the line: `server_url=None`
   - Change to: `server_url="YOUR_WEB_APP_URL"`

7. **Test**:
   - Run the game, answer a quiz question
   - Check your Google Sheet for the new row

### What Gets Logged

Each quiz result creates a row with:
- Timestamp
- Question ID
- Question text
- Whether answer was correct
- Coins earned

## Customization

### Add More Questions

Edit `src/quiz/questions.json`:

```json
{
  "id": 9,
  "question": "Your question here?",
  "choices": [
    "Choice A",
    "Choice B", 
    "Choice C",
    "Choice D"
  ],
  "correct": 0,
  "explanation": "Explanation of the answer"
}
```

### Change Quiz Timing

In `src/snake_game.py`, modify:
```python
QUIZ_INTERVAL_SECONDS = 180  # Change this number (in seconds)
```

### Add More Prizes

In `src/store.py`, edit the `PRIZES` list:
```python
PRIZES = [
    "Your New Prize",
    "Another Prize",
    # ... add more
]
```

### Change Game Speed

In `src/snake_game.py`, modify:
```python
GAME_SPEED = 10  # Higher = faster, Lower = slower
```

## Educational Use

This game demonstrates several programming concepts for students:

1. **Game Loop**: Continuous update and render cycle
2. **Collision Detection**: Snake vs walls, snake vs self, snake vs apple
3. **Event Handling**: Keyboard input, quiz timing
4. **Data Persistence**: Saving/loading JSON files
5. **API Integration**: POSTing data to web endpoints
6. **Callbacks**: Quiz pause/resume mechanism
7. **State Management**: Game states, quiz active/inactive

## Troubleshooting

**Game won't start:**
- Ensure Python 3.8+ is installed: `python --version`
- Install dependencies: `pip install -r requirements.txt`

**Quiz doesn't appear:**
- Check that `src/quiz/questions.json` exists
- Wait the full interval (or enable demo mode)

**Store won't save:**
- Check file permissions in the directory
- Look for `store_state.json` file

**Backend not working:**
- Verify the web app URL is correct
- Check the SECRET_TOKEN matches
- Ensure the sheet is not deleted

## License

Part of the spaceForce educational project. See root LICENSE file.

## Credits

Developed as an MVP to demonstrate:
- Educational game design
- Quiz integration in games
- Backend data collection for learning analytics
