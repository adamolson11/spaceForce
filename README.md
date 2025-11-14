# Space Force 🚀
Educational game platform teaching kids OOP and coding concepts through space-themed games.

## Overview
Space Force combines browser-based games (HTML/JavaScript) with Unity prototypes (C#) to create an engaging learning environment. Students explore the solar system, learn programming concepts, and earn coins through quiz challenges.

## Quick Start

### Play Browser Games (No Installation)
1. Open `index.html` in your browser
2. Select a game from the portal
3. Enjoy instant space adventures!

### Unity Development (Game Engine)
**New to Unity?** Start here:
- 📖 **[Unity Integration Guide](UNITY_INTEGRATION_GUIDE.md)** - Complete beginner's guide
- 🔗 **[Unity to Browser Connection](UNITY_TO_BROWSER_CONNECTION.md)** - How systems work together
- 📋 **[Assets Overview](Assets/README_UNITY_BASICS.md)** - What's already built

**Quick Setup**:
1. Install Unity 2023.4 LTS
2. Open project in Unity Hub
3. Window → Planet Asset Importer → Download Textures
4. Open `Assets/Graphics/Scenes/DemoScene.unity`
5. Press Play!

See [UNITY_SETUP.md](UNITY_SETUP.md) for detailed instructions.

## Project Structure

```
spaceForce/
├── 🌐 Browser Games (Live Now)
│   ├── index.html - Entry point
│   ├── gamePortal.html - Game selection
│   └── games/
│       ├── rpg_adventure_3d.html - 3D space explorer (Three.js)
│       └── [other games...]
│
├── 🎮 Unity Prototypes (Development)
│   └── Assets/
│       ├── Scripts/ - C# game logic
│       ├── Graphics/ - NASA textures & materials
│       └── Editor/ - Automation tools
│
└── 📚 Documentation
    ├── UNITY_INTEGRATION_GUIDE.md - Beginner's guide
    ├── UNITY_TO_BROWSER_CONNECTION.md - Integration strategy
    ├── UNITY_SETUP.md - Detailed setup
    └── Assets/README_UNITY_BASICS.md - What's built
```

## Features

### Browser Games
- **3D Space RPG**: Explore solar system with realistic planets
- **Space Shooter**: Wave-based OOP combat game
- **Python Snake**: Learn Python with Brython
- **Quiz System**: Earn coins answering questions

### Unity Prototypes
- **NASA Textures**: High-resolution planet textures (2K)
- **Physics-Based**: Realistic ship controls with Rigidbody
- **Object Pooling**: Performance optimization patterns
- **Automated Importer**: One-click NASA asset download

## For Educators

### Quiz System
- Timed quizzes integrated into gameplay
- Custom questions via `src/quiz/questions.json`
- Google Sheets backend for tracking
- 10 coins per correct answer

### Educational Concepts Taught
- Object-Oriented Programming (OOP)
- Inheritance and polymorphism
- Object pooling patterns
- Physics simulations
- Event handling
- Game loops and delta time

## Getting Started with Unity

**Never used Unity before?** We've got you covered:

1. **Read the Guide**: [UNITY_INTEGRATION_GUIDE.md](UNITY_INTEGRATION_GUIDE.md)
   - Installation walkthrough
   - Interface explanation
   - Your first scene tutorial
   - Common mistakes to avoid

2. **Understand the Connection**: [UNITY_TO_BROWSER_CONNECTION.md](UNITY_TO_BROWSER_CONNECTION.md)
   - How Unity and browser games relate
   - Integration strategies
   - Practical examples

3. **Explore What's Built**: [Assets/README_UNITY_BASICS.md](Assets/README_UNITY_BASICS.md)
   - Script documentation
   - How to use existing components
   - Quick reference guide

## Technology Stack

**Browser Games**:
- Vanilla JavaScript (ES6+)
- Three.js v0.156.0 (3D graphics)
- Bootstrap 5.3 (UI)
- Brython (Python-in-browser)

**Unity Prototypes**:
- Unity 2023.4 LTS
- C# scripting
- Universal Render Pipeline (URP)
- NASA public domain textures

## Development

### Browser Game Development
```bash
# No build step - just open in browser
open index.html
```

### Unity Development
```bash
# First time
cd spaceForce
# Open in Unity Hub → Add → Select folder

# In Unity Editor
# Window → Planet Asset Importer → Download Textures
# Open DemoScene.unity
# Press Play ▶️
```

## Documentation

- **Unity Guides**:
  - [UNITY_INTEGRATION_GUIDE.md](UNITY_INTEGRATION_GUIDE.md) - Start here if new to Unity
  - [UNITY_TO_BROWSER_CONNECTION.md](UNITY_TO_BROWSER_CONNECTION.md) - Integration overview
  - [UNITY_SETUP.md](UNITY_SETUP.md) - Detailed setup instructions
  - [QUICK_START_UNITY.md](QUICK_START_UNITY.md) - Condensed checklist
  - [Assets/README_UNITY_BASICS.md](Assets/README_UNITY_BASICS.md) - Script documentation

- **Browser Game Docs**:
  - [CONVERSION_SUMMARY.md](CONVERSION_SUMMARY.md) - 2D to 3D conversion story
  - [README_SNAKE.md](README_SNAKE.md) - Python snake game docs

- **Assets**:
  - [Assets/ASSETS.md](Assets/ASSETS.md) - NASA texture sources and licensing

## Contributing

1. Choose your platform (Browser or Unity)
2. Read relevant documentation
3. Follow existing code patterns (OOP, object pooling)
4. Test in multiple browsers/platforms
5. Include educational comments for students

## License

NASA textures are public domain - credit line required:
"Planetary textures courtesy of NASA"

See [LICENSE](LICENSE) for code licensing.

## Resources

- **Unity Learning**: https://learn.unity.com
- **Three.js Docs**: https://threejs.org/docs
- **NASA Textures**: https://solarsystem.nasa.gov/resources/

---

**Questions?** Check the documentation guides above or open a GitHub issue! 
