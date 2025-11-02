# 3D Space RPG Adventure

## Overview
A 3D educational game that lets players explore our solar system in immersive 3D graphics. Players can visit all 8 planets plus the Sun, learning about each celestial body while mastering 3D navigation.

## Features

### 3D Graphics
- Built with Three.js (WebGL)
- Real-time 3D rendering
- 5,000+ stars background
- Realistic lighting from the Sun
- Planet glows and visual effects
- Saturn's rings

### Dual Camera Modes
1. **Top View** - Bird's-eye perspective showing the entire solar system layout
2. **3D View** - Third-person camera that follows the spaceship with mouse control

### Educational Content
Each planet includes real astronomical information:
- **Mercury**: Smallest planet, closest to the Sun
- **Venus**: Hottest planet with thick atmosphere
- **Earth**: Our home, only known planet with life
- **Mars**: The Red Planet with largest volcano
- **Jupiter**: Largest planet, gas giant
- **Saturn**: Famous for its beautiful rings
- **Uranus**: Ice giant tilted on its side
- **Neptune**: Farthest planet with strongest winds

### Controls
- **Movement**: W/A/S/D or Arrow Keys
- **Look**: Move mouse to rotate camera (3D View mode)
- **View Toggle**: Click buttons to switch between camera modes
- **Planet Info**: Automatically displays when near planets

### Game Mechanics
- Free 3D movement through space
- Proximity detection for planets
- Distance tracking
- Coin system integration (for future features)
- Persistent student profile

## Technical Implementation

### Architecture
- Single HTML file with embedded JavaScript
- Three.js for 3D rendering
- WebGL renderer with antialiasing
- No external dependencies beyond Three.js

### Performance
- Optimized geometry using BufferGeometry
- Efficient particle system for stars
- Smooth 60 FPS animation loop
- Responsive to window resize

### Security
- No dangerous functions (eval, innerHTML, etc.)
- Uses textContent for safe DOM updates
- Local script loading only
- No external CDN dependencies at runtime

## Differences from 2D Version

| Feature | 2D Version | 3D Version |
|---------|-----------|-----------|
| Graphics | Canvas 2D | Three.js WebGL 3D |
| Camera | Fixed top-down | Dual mode (top/3D) |
| Movement | 2D plane | Full 3D space |
| Planets | 2D circles | 3D spheres with effects |
| Lighting | None | Dynamic lighting from Sun |
| Stars | 200 static dots | 5,000 3D particles |
| Visuals | Flat colors | Materials, glows, shadows |

## Browser Requirements
- Modern browser with WebGL support
- Recommended: Chrome, Firefox, Edge, Safari (latest versions)
- Hardware acceleration enabled

## Future Enhancements
- Space monsters and enemies
- Quiz integration for planet facts
- Planet missions and quests
- Special abilities and power-ups
- Multiplayer support
- VR mode support

## Files
- `rpg_adventure_3d.html` - Main game file (self-contained)
- `../libs/three.min.js` - Three.js library

## How to Play
1. Open `rpg_adventure_3d.html` in a web browser
2. Use WASD or arrow keys to move your spaceship
3. Move mouse to look around in 3D view
4. Click view buttons to toggle camera modes
5. Fly close to planets to learn about them
6. Track your distance traveled

## Development Notes
- Created as part of the spaceForce educational game project
- Maintains all educational content from 2D version
- Designed to be engaging for students learning programming
- Can be extended with quiz integration for OOP learning

## Credits
- Built with Three.js (https://threejs.org/)
- Part of the spaceForce educational game platform
- Solar system data based on real astronomical information
