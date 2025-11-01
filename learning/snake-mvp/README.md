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
