# Snake Learning MVP

## Overview

This is a self-contained static web MVP that teaches kids how a simple Snake game is built using Python (Brython) in the browser. The MVP includes:

- **Mock Sign-In**: Simple authentication that stores student name in localStorage
- **Portal**: Main game and learning interface
- **Snake Game**: Classic Snake game built with Python/Brython
- **Quiz System**: 6-question multiple-choice quiz that awards "gold coins" stored in localStorage
- **Show Code**: Panel that maps quiz items to actual game code
- **In-Browser Editor**: Simple code editor where students can modify Python code and re-run the game
- **Teacher Dashboard**: Stub page that reads student progress from localStorage (extendable)

## How to Run Locally

1. Open `index.html` in a modern web browser (Chrome, Firefox, Safari, or Edge)
2. Enter your name on the sign-in page
3. You'll be redirected to the Snake game learning portal (`snake.html`)

**No build step required!** This is a static HTML/CSS/JavaScript application using Brython for Python execution in the browser.

## Teaching Workflow

### For Students:
1. **Sign In**: Enter your name on the landing page
2. **Play the Game**: Use arrow keys to control the snake and collect food
3. **Take the Quiz**: After playing, click "Take Quiz" to answer questions about how the game works
4. **Earn Coins**: Each correct answer awards gold coins (stored locally)
5. **View Code**: Click "Show Code" to see the actual Python code that makes the game work
6. **Edit & Experiment**: Use the built-in editor to modify the game code and click "Run Edited Code" to see your changes

### For Teachers:
1. Open `teacher-dashboard.html` to view a stub dashboard
2. The dashboard reads student progress from browser localStorage
3. Can be extended to show multiple students' coin balances and quiz scores

## Project Structure

```
learning/snake-mvp/
├── README.md              # This file
├── index.html             # Sign-in page
├── snake.html             # Main game + learning page
├── teacher-dashboard.html # Teacher/admin dashboard (stub)
├── style.css              # Shared styles
├── snake_game.py          # Python code for Snake game (Brython)
├── quiz_data.py           # Quiz questions and answers
└── api/                   # Backend stubs for future extensions
    └── README.md          # Backend extension guide
```

## Extension Points

### 1. In-Browser Code Editor Enhancement
**Current**: Simple textarea with "Run Edited Code" button
**Future Improvements**:
- Integrate CodeMirror or Monaco Editor for syntax highlighting
- Add Python linting and error checking
- Provide code templates and hints
- Add undo/redo functionality

**Files to Modify**: `snake.html` (editor section)

### 2. Teacher/Admin Dashboard
**Current**: Stub page reading from localStorage
**Future Improvements**:
- Connect to backend API for multi-student data
- Add charts/graphs for student progress
- Filter and sort students by performance
- Export reports

**Files to Modify**: `teacher-dashboard.html`, `api/endpoints.js` (create)

### 3. Backend API for Persistence
**Current**: All data stored in browser localStorage
**Future Improvements**:
- User authentication with JWT tokens
- Store student progress in a database
- RESTful API for CRUD operations
- Real-time progress updates via WebSockets

**Files to Add**: See `api/README.md` for backend architecture guide

### 4. Additional Learning Content
**Ideas**:
- Add more quiz questions about Python concepts
- Include code challenges with automated tests
- Add video tutorials or animated explanations
- Create different difficulty levels
- Add other game examples (Pong, Tetris, etc.)

**Files to Modify**: `quiz_data.py`, create new game modules

## Technologies Used

- **Brython**: Python interpreter for browsers (https://brython.info/)
- **HTML5 Canvas**: For game rendering
- **localStorage**: Client-side data persistence
- **Bootstrap/Custom CSS**: Responsive styling
- **Vanilla JavaScript**: UI interactions and DOM manipulation

## Browser Compatibility

Works in all modern browsers that support:
- ES6 JavaScript
- HTML5 Canvas API
- localStorage API
- CSS3

Tested in: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+

## License

Same as parent project (see root LICENSE file)
