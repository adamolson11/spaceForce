# Snake Game MVP - Learn Python with Brython

## Overview
This is a self-contained static web MVP for teaching kids how to build a Snake game using Brython (Python in the browser). The MVP runs entirely in the browser with no server required.

## How to Run Locally
Simply open `index.html` in a modern web browser (Chrome, Firefox, Safari, or Edge). No server or installation required!

1. Open `index.html` - Sign in with your name or play as guest
2. You'll be taken to `snake.html` - the main learning and game page
3. Start playing Snake and learning Python!

## Features

### Quiz and Coins Flow
- Click "Take Quiz" to open a modal with 6 multiple-choice questions about Python and game development
- Each correct answer earns you 10 coins
- Your total coins are displayed in the header
- Coins are stored in localStorage and persist between sessions
- Quiz progress is tracked so you can retake it to improve your score

### Code Editor
- Click "Show Code" to reveal Python code snippets that power the game
- Use the Editor area to modify the Snake game code
- Click "Run Edited Code" to save your changes to localStorage
- Reload the page to see your changes in action
- Your custom code is stored under the key `student_custom_snake` in localStorage

### Game Controls
- Use arrow keys to control the snake
- Click "Start" to begin the game
- Click "Pause" to pause the game
- Click "Restart" to reset and start over
- Try to eat the food (red squares) to grow your snake and earn points

## Security Warning ⚠️
**IMPORTANT**: This MVP uses `localStorage` to store and evaluate user code. This approach is **UNSAFE for production** because:
- Evaluating code from localStorage can execute arbitrary JavaScript/Python
- There's no sandboxing or validation of user input
- No authentication or authorization
- Data is stored unencrypted in the browser

This is intended as a **learning prototype only**, not for production use.

## Next Steps for Production

### 1. Backend Integration
- [ ] Set up a proper backend API (Node.js/Express, Python/Flask, or similar)
- [ ] Implement database storage for users, progress, and code
- [ ] Create RESTful endpoints (see `api/README.md` for stubs)
- [ ] Add proper error handling and validation

### 2. Authentication & Authorization
- [ ] Implement real user authentication (OAuth, JWT, etc.)
- [ ] Add role-based access control (student vs teacher vs admin)
- [ ] Secure session management
- [ ] Password hashing and secure storage

### 3. Code Editor Improvements
- [ ] Integrate CodeMirror or Monaco Editor for syntax highlighting
- [ ] Add autocomplete and error detection
- [ ] Implement code formatting and linting
- [ ] Add keyboard shortcuts and themes

### 4. Code Sandboxing & Security
- [ ] Use Web Workers to isolate code execution
- [ ] Implement iframe sandboxing for running user code
- [ ] Add code validation and sanitization
- [ ] Set up Content Security Policy (CSP) headers
- [ ] Implement rate limiting for code execution

### 5. Teacher Dashboard
- [ ] Create admin interface for managing students
- [ ] Add progress tracking and analytics
- [ ] Implement quiz creation and management tools
- [ ] Add classroom/group management features

### 6. Additional Features
- [ ] Multi-level progression system
- [ ] More interactive tutorials
- [ ] Peer code sharing and collaboration
- [ ] Leaderboards and achievements
- [ ] Mobile-responsive design improvements

## Technology Stack
- **Brython**: Python interpreter that runs in the browser
- **HTML5 Canvas**: For rendering the Snake game
- **LocalStorage**: For persisting user data (temporary solution)
- **Bootstrap** (optional): For responsive UI components

## File Structure
```
learning/snake-mvp/
├── README.md (this file)
├── index.html (sign-in page)
├── snake.html (main learning page)
├── snake.py (Brython Snake game code)
├── quiz_data.py (Python quiz questions)
└── api/
    └── README.md (backend API stubs and documentation)
```

## Contributing
This is an educational project. Feel free to enhance it by:
- Adding more quiz questions
- Creating additional game levels
- Improving the UI/UX
- Adding more code examples and tutorials

## License
Part of the spaceForce educational project.
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
