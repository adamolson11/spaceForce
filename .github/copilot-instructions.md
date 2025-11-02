# SpaceForce Project - AI Agent Instructions

## Project Overview
Educational game platform teaching kids OOP and coding concepts through space-themed games. **Dual architecture**: browser-based games (HTML/JS/Three.js) + Unity C# prototypes.

## Core Architecture

### Frontend Structure
- **Portal System**: `index.html` → `gamePortal.html` → individual games
- **2D Games**: Canvas 2D API (`script.js`, `playPage.html` - Space Shooter)
- **3D Games**: Three.js WebGL (`games/rpg_adventure_3d.html`, `prototype/main.js`)
- **Educational Games**: Brython-based Python learning (`learning/snake-mvp/`)

### Technology Stack
**Browser Games:**
- Vanilla JS with OOP class patterns (no frameworks)
- Three.js v0.156.0 for 3D (installed locally in `libs/`)
- Brython for Python-in-browser (`learning/snake-mvp/`)
- Bootstrap 5.3 for UI styling
- Canvas 2D API for classic games

**Unity Prototypes:**
- C# scripts in `Assets/Scripts/` (ShipController, ObjectPool, OrbitIntegrator, etc.)
- Designed for Unity 2023.4 LTS with URP
- NASA public-domain textures planned (see `Assets/ASSETS.md`)

### Key Games
1. **Space Shooter** (`playPage.html` + `script.js`): 2D wave-based OOP shooter teaching classes, inheritance, object pooling
2. **3D Space RPG** (`games/rpg_adventure_3d.html`): Educational solar system exploration with dual camera modes
3. **Snake MVP** (`learning/snake-mvp/`): Brython-based Python teaching tool with quiz system

## Critical Patterns

### OOP Architecture (2D Games)
All entities use class-based inheritance:
```javascript
class Game {
  constructor(canvas) { /* centralized state */ }
  render(context, deltaTime) { /* game loop */ }
  checkCollision(a, b) { /* universal collision */ }
}
class Enemy { /* base class */ }
class Beetlemorph extends Enemy { /* specific enemy */ }
```
**Never use functional components** - maintain OOP style for educational consistency.

### Object Pooling Pattern
Critical for performance in shooters (see `script.js`):
```javascript
this.projectilesPool = []; // Pre-allocated projectiles
getProjectile() { return this.projectilesPool.find(p => p.free); }
projectile.reset() { this.free = true; } // Return to pool
```
Always reuse objects with `.free` flag rather than instantiate/destroy.

### 3D Scene Setup (Three.js)
Standard pattern in all 3D games:
```javascript
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(fov, aspect, near, far);
const renderer = new THREE.WebGLRenderer({ antialias: true });
// Dual camera modes: orthographic top-view + 3D third-person
```
Use local Three.js from `libs/three.min.js` - no CDN dependencies.

### Quiz System Integration
Python quiz manager pattern (`src/quiz/quiz_manager.py`):
- Timed quizzes (default 180s intervals, 10s in demo mode)
- Pause/resume callbacks for game integration
- Google Apps Script backend (`server/google_apps_script.gs`)
- 10 coins per correct answer
- Results stored locally + optionally POST to server

## File Conventions

### Self-Contained Games
Games are **single-file monoliths** by design (educational simplicity):
- `games/rpg_adventure_3d.html` - complete game in one HTML file (~750 lines)
- Embedded CSS in `<style>` blocks
- Embedded JS with full game logic
- Only external dependency: Three.js from `libs/`

### Asset References
Images loaded via `document.getElementById()` from HTML:
```html
<img id="player" src="images/player.png" style="display:none">
```
Then used in canvas: `context.drawImage(this.image, ...)`

### Python/Brython Games
Located in `learning/snake-mvp/`:
- `snake_game.py` - main game logic in Python
- `snake.html` - includes Brython CDN + quiz system
- `quiz_data.py` - Python quiz questions
- **Security warning**: Uses `localStorage` eval - unsafe for production

## Development Workflows

### Running Games Locally
No build step required - pure static files:
```bash
# Just open in browser:
# index.html → gamePortal.html → select game
# OR directly open any game HTML file
```

### Adding New Games
1. Create self-contained HTML in `games/` directory
2. Add card entry to `gamePortal.html`:
```html
<div class="game-card">
  <div class="game-card-icon">🎮</div>
  <h3>Game Title</h3>
  <a href="games/your_game.html" class="btn btn-game">Play Now</a>
</div>
```
3. Follow OOP pattern - extend `Game` base class if applicable

### Dependencies
**JavaScript:**
- Three.js: `npm install three` (already done)
- Located in `libs/` for offline use
- Version: 0.156.0

**Python (for backend/quiz system):**
```bash
pip install -r requirements.txt
# pygame==2.5.2, requests==2.31.0
```

### Unity Development

**Quick Setup (One-Click Import):**
```
1. Open project in Unity 2023.4 LTS
2. Window → Planet Asset Importer → Open
3. Click "Download Textures & Create Prefabs"
4. All assets created automatically (textures, materials, prefabs, demo scene)
```

See `UNITY_SETUP.md` for complete setup guide.

**C# Script Conventions:**
- `[RequireComponent(typeof(Rigidbody))]` attributes
- Physics-based movement with Rigidbody
- Object pooling for projectiles
- See `Assets/Scripts/` for reference implementations

**Editor Tools:**
- `Assets/Editor/PlanetAssetImporter.cs` - Automated NASA texture downloader
- `Assets/Editor/PackageBuilder.cs` - Export assets as .unitypackage

## Integration Points

### Student Profile System
Persistent storage pattern (all games):
```javascript
localStorage.setItem('studentName', name);
localStorage.setItem('coins', totalCoins);
// Displayed in header across all pages
```

### Quiz Integration Flow
1. Game includes `QuizManager` instance
2. Calls `check_and_show_quiz()` in game loop
3. Pauses game when quiz triggers
4. Awards coins on correct answers
5. Resumes game after submission

### Google Sheets Backend
Optional server integration via `server/google_apps_script.gs`:
- Deploy as web app
- POST quiz results: `{timestamp, question_id, correct, coins_earned}`
- Requires SECRET_TOKEN configuration

## Visual/Style Standards

### UI Theme
Glassmorphism + space theme:
```css
background: rgba(255, 255, 255, 0.1);
backdrop-filter: blur(10px);
border-radius: 10px;
/* Animated starfield backgrounds */
```

### Particle Effects
All games include explosion particles:
```javascript
class Particle {
  update() { this.life -= this.decay; }
  draw(context) { context.globalAlpha = this.life; }
}
```

### Camera Modes (3D Games)
Always provide dual modes:
- **Top View**: Orthographic for spatial understanding
- **3D View**: Third-person with mouse-look for immersion

## Common Pitfalls

❌ **Don't** use external CDNs for Three.js - use local `libs/` copy
❌ **Don't** use `innerHTML` - security risk (use `textContent`)
❌ **Don't** break OOP patterns - maintain class-based architecture
❌ **Don't** use functional React/Vue patterns - this is vanilla JS educational code
❌ **Don't** create multi-file builds - games should be self-contained

✅ **Do** follow object pooling for projectiles/particles
✅ **Do** use `requestAnimationFrame` for game loops
✅ **Do** maintain delta time for frame-rate independence
✅ **Do** include educational comments for students
✅ **Do** test in multiple browsers (Chrome, Firefox, Safari, Edge)

## Recent Major Changes

See `CONVERSION_SUMMARY.md` for 2D→3D RPG conversion details (completed 2025-11-02). Key lesson: maintained all educational content while upgrading graphics engine.

## Documentation Standards

When creating new features:
1. Add game card to `gamePortal.html`
2. Include README in `games/README_[GAME].md` if complex
3. Document any Unity assets in `Assets/ASSETS.md`
4. Update quiz questions in `src/quiz/questions.json` if adding new concepts

## Questions to Ask Before Coding

1. Does this game teach a specific coding concept? (OOP, loops, arrays, etc.)
2. Can it be self-contained in one HTML file?
3. Does it follow the existing OOP class patterns?
4. Will it work offline without external dependencies?
5. Is it appropriate for kids learning to code?
