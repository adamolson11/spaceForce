# Unity Assets Overview
## What's Already Built in This Project

This document explains what Unity components exist in the Space Force project and how to use them.

---

## Quick Status Check

### ✅ What's Ready to Use
- **C# Scripts** - Complete and functional
- **Editor Tools** - NASA texture importer ready
- **Asset Importer** - One-click setup for planets
- **Project Structure** - Folders organized and ready

### ⬜ What Needs Setup (By You)
- **NASA Textures** - Run the importer to download
- **Materials** - Created automatically by importer
- **Prefabs** - Created automatically by importer
- **Demo Scene** - Created automatically by importer

---

## File Structure Explained

```
Assets/
│
├── Scripts/                    ← C# game logic
│   ├── ShipController.cs       ✅ Ready - Ship movement
│   ├── PlanetController.cs     ✅ Ready - Planet rotation
│   ├── Projectile.cs           ✅ Ready - Bullets/projectiles
│   ├── ObjectPool.cs           ✅ Ready - Performance optimization
│   └── OrbitIntegrator.cs      ✅ Ready - Realistic orbit physics
│
├── Editor/                     ← Unity Editor extensions
│   ├── PlanetAssetImporter.cs  ✅ Ready - Downloads NASA textures
│   └── PackageBuilder.cs       ✅ Ready - Exports asset packages
│
├── Graphics/                   ⬜ Created by importer
│   ├── Planets/                ⬜ NASA texture files (PNG)
│   ├── Materials/              ⬜ Unity materials for planets
│   ├── Prefabs/                ⬜ Reusable planet objects
│   └── Scenes/                 ⬜ Demo solar system scene
│
├── ASSETS.md                   ✅ Documentation
├── README_UNITY_BASICS.md      ✅ This file
└── download_assets.sh          ✅ Alternative shell script
```

---

## The C# Scripts (What They Do)

### 1. ShipController.cs
**Purpose**: Makes a spaceship move and shoot

**What it does**:
- W/S keys = forward/backward thrust
- A/D keys = rotate left/right
- Space = fire projectile
- Uses Unity physics (Rigidbody)

**How to use**:
1. Create a GameObject (e.g., empty object with cube child)
2. Add component → ShipController
3. Add component → Rigidbody (required)
4. Set "Use Gravity" to OFF on Rigidbody
5. Assign projectile prefab in Inspector (optional)
6. Play and use WASD + Space!

**Code snippet**:
```csharp
[RequireComponent(typeof(Rigidbody))]
public class ShipController : MonoBehaviour
{
    public float thrustForce = 20f;
    public float rotationSpeed = 90f;
    // ...
}
```

---

### 2. PlanetController.cs
**Purpose**: Makes planets rotate and optionally orbit

**What it does**:
- Rotates planet on its axis (day/night cycle)
- Optional: Orbit around a central point (like Sun)
- Configurable rotation speed and axial tilt

**How to use**:
1. Create a sphere GameObject
2. Add component → PlanetController
3. Set rotation speed (e.g., 10 degrees/second)
4. Set axial tilt (e.g., 23 for Earth)
5. Optional: Enable orbit and set center point
6. Play and watch it spin!

**Inspector settings**:
- Rotation Degrees Per Second: `10` = slow spin
- Axial Tilt Degrees: `23` = Earth-like tilt
- Use Orbit: `true` to enable circular orbit
- Orbit Center: Drag Sun GameObject here
- Orbit Radius: Distance from center
- Orbit Period Seconds: Time for one orbit

---

### 3. Projectile.cs
**Purpose**: Bullets/lasers that fly and despawn

**What it does**:
- Moves forward at set speed
- Auto-destroys after lifetime
- Designed to work with ObjectPool (optional)

**How to use**:
1. Create small object (sphere/capsule)
2. Add component → Projectile
3. Add component → Rigidbody
4. Set lifetime (e.g., 3 seconds)
5. Save as prefab
6. Assign to ShipController's projectilePrefab field

---

### 4. ObjectPool.cs (Advanced)
**Purpose**: Performance optimization for frequently spawned objects

**What it does**:
- Reuses objects instead of creating/destroying
- Prevents garbage collection lag
- Used for projectiles, particles, effects

**When to use**:
- Spawning 100+ objects per second
- Projectiles, particles, enemies
- Not needed for planets or ships

**How it works**:
```csharp
// Instead of:
Instantiate(projectile);  // Creates new object (slow)

// Use pool:
GameObject obj = objectPool.GetFromPool();  // Reuses object (fast)
```

---

### 5. OrbitIntegrator.cs (Advanced)
**Purpose**: Realistic orbital mechanics using physics

**What it does**:
- Calculates gravitational forces
- Applies to moving bodies (ships, asteroids)
- More accurate than simple circular orbits

**When to use**:
- Realistic space flight simulation
- N-body gravitational systems
- Advanced physics gameplay

**Not needed for basic game** - use PlanetController's simple orbit instead.

---

## The Editor Tools

### Planet Asset Importer
**Location**: Window → Planet Asset Importer → Open

**What it does**:
1. Downloads NASA textures from official sources
2. Creates 3 resolutions per planet (2048, 1024, 512)
3. Generates Saturn ring texture
4. Creates Unity materials with URP shaders
5. Builds planet prefabs (ready to drag-and-drop)
6. Creates DemoScene.unity with full solar system

**When to run it**:
- First time setting up project
- When you want to update/refresh textures
- After corrupting or deleting Graphics folder

**How to use**:
1. Menu: Window → Planet Asset Importer → Open
2. Click "Download Textures & Create Prefabs" button
3. Wait 2-5 minutes (downloads ~50 MB from NASA)
4. Check `Assets/Graphics/` folder for results
5. Open `Assets/Graphics/Scenes/DemoScene.unity`
6. Press Play to see solar system!

**What NASA textures does it get**:
- Sun (emissive glowing material)
- Mercury, Venus, Earth, Mars
- Jupiter, Saturn (with rings)
- Uranus, Neptune
- Saturn's rings (separate transparent texture)

---

### Package Builder
**Location**: Window → Package Builder → Open

**What it does**:
- Exports all planet assets as `.unitypackage` file
- Others can import without running importer
- Useful for sharing with team/students

**When to use**:
- Sharing project with others
- Backing up assets
- Distributing to students without internet

**How to use**:
1. Window → Package Builder → Open
2. Click "Build Planet Assets Package"
3. Package saved to `Builds/PlanetAssets.unitypackage`
4. Others import via: Assets → Import Package → Custom Package

**Alternative quick method**:
- Menu: Tools → SpaceForce → Build Planet Package (Quick)

---

## Quick Start Workflow

### First Time Setup (15 minutes)

```
Step 1: Open Unity Project
├─ Open Unity Hub
├─ Click "Add" or "Open"
├─ Select spaceForce folder
└─ Unity imports (wait 2-5 minutes)

Step 2: Set Up URP (if not already)
├─ Edit → Project Settings → Graphics
├─ If empty, create URP asset:
│  └─ Right-click Project → Create → Rendering → URP Asset
└─ Assign to Scriptable Render Pipeline Settings

Step 3: Run Planet Asset Importer
├─ Window → Planet Asset Importer → Open
├─ Click "Download Textures & Create Prefabs"
└─ Wait for completion (~2-5 min)

Step 4: Verify Assets Created
└─ Check Assets/Graphics/ for:
   ├─ Planets/ (textures)
   ├─ Materials/ (materials)
   ├─ Prefabs/ (planet prefabs)
   └─ Scenes/DemoScene.unity

Step 5: Test Demo Scene
├─ Open Assets/Graphics/Scenes/DemoScene.unity
├─ Press Play (▶️)
└─ You should see solar system!

✅ Done! Assets are ready to use.
```

---

## Using the Assets in Your Scene

### Add a Planet to Your Scene

**Method 1: Use Prefab (Easy)**
1. Open your scene
2. Navigate to `Assets/Graphics/Prefabs/`
3. Drag `Planet_Earth.prefab` into Hierarchy
4. Position it where you want (Inspector → Transform)
5. Done! It has texture and rotation script already

**Method 2: From Scratch (Learning)**
1. GameObject → 3D Object → Sphere
2. Scale it (e.g., 3, 3, 3)
3. Add Component → PlanetController
4. In Project, find `Assets/Graphics/Materials/Planet_Earth.mat`
5. Drag material onto sphere
6. Done!

---

### Add a Controllable Ship

**Steps**:
1. GameObject → Create Empty → Name it "PlayerShip"
2. Right-click PlayerShip → 3D Object → Cube (child)
3. Scale cube to look ship-like (1, 0.3, 2)
4. Select PlayerShip (parent)
5. Add Component → ShipController
6. Add Component → Rigidbody
7. In Rigidbody: Uncheck "Use Gravity"
8. Position ship away from planets (e.g., 0, 0, 10)
9. Press Play, use WASD to fly!

---

### Add Camera

If your scene doesn't have one:

1. GameObject → Camera
2. Position it to view your scene (e.g., 0, 50, 100)
3. Rotate to look at planets (Inspector → Rotation)
4. Or attach camera to ship for first-person view:
   - Drag camera onto PlayerShip in Hierarchy (makes it child)
   - Position: (0, 5, -10) relative to ship
   - Rotation: (10, 0, 0) to tilt down slightly

---

## Common Tasks

### Change Planet Texture
1. Find material in `Assets/Graphics/Materials/`
2. Select it
3. In Inspector, click texture box
4. Choose new texture from `Assets/Graphics/Planets/`

### Make Planet Spin Faster/Slower
1. Select planet in Hierarchy
2. Find PlanetController component in Inspector
3. Change "Rotation Degrees Per Second" value
4. Press Play to test

### Adjust Ship Speed
1. Select ship in Hierarchy
2. Find ShipController component
3. Change "Thrust Force" value (higher = faster)
4. Press Play to test

### Add Projectile Shooting
1. Create projectile prefab:
   - GameObject → 3D Object → Capsule
   - Scale small (0.2, 0.5, 0.2)
   - Add Rigidbody component
   - Add Projectile component
   - Drag to Project to make prefab
   - Delete from scene

2. Assign to ship:
   - Select PlayerShip
   - Find ShipController
   - Drag projectile prefab to "Projectile Prefab" field
   - Optionally: Create empty child "FirePoint" and assign

3. Test:
   - Press Play
   - Press Space to fire!

---

## Troubleshooting

### "Materials are pink/magenta"
**Cause**: URP not set up or shader incompatible

**Fix**:
1. Edit → Project Settings → Graphics
2. Ensure URP asset is assigned
3. Or: Select material → Inspector → Shader dropdown → Universal Render Pipeline → Lit

---

### "Ship won't move"
**Causes**:
- Missing Rigidbody
- Gravity enabled
- Script not attached
- Game window not focused

**Fixes**:
1. Check Rigidbody attached to ship
2. Rigidbody → Uncheck "Use Gravity"
3. Check ShipController attached
4. Click Game window to focus it
5. Check Console for errors

---

### "Can't find Planet Asset Importer menu"
**Cause**: Script error or Unity didn't compile

**Fix**:
1. Check Console for red errors
2. Window → Assets → Reimport All
3. Restart Unity Editor
4. Verify file exists: `Assets/Editor/PlanetAssetImporter.cs`

---

### "Downloads failing in Planet Asset Importer"
**Cause**: Network issues or NASA servers

**Fix**:
1. Check internet connection
2. Try again later
3. Use manual shell script: `cd Assets && ./download_assets.sh`
4. Or download manually from NASA websites (see ASSETS.md)

---

## Next Steps

### After Setup:
1. ✅ Run Planet Asset Importer
2. ✅ Open DemoScene and explore
3. → Create your own scene
4. → Add ship with ShipController
5. → Add planets with PlanetController
6. → Test and experiment!

### Learning Resources:
- Read script comments in `Assets/Scripts/` files
- See `UNITY_INTEGRATION_GUIDE.md` for Unity basics
- See `UNITY_TO_BROWSER_CONNECTION.md` for integration strategy
- See `ASSETS.md` for NASA texture licensing info

### Ideas to Try:
- Add more planets
- Create asteroid field
- Make a simple space station
- Add collectible coins
- Integrate quiz system from browser game
- Add particle effects for thrust

---

## Script API Quick Reference

### ShipController
```csharp
public float thrustForce;      // Movement power
public float rotationSpeed;    // Turn rate
public GameObject projectilePrefab;  // What to shoot
public Transform firePoint;    // Where to spawn projectile
```

### PlanetController
```csharp
public Material planetMaterial;          // Texture material
public float rotationDegreesPerSecond;   // Spin speed
public float axialTiltDegrees;           // Tilt angle
public bool useOrbit;                    // Enable orbiting
public Transform orbitCenter;            // What to orbit around
public float orbitRadius;                // Distance from center
public float orbitPeriodSeconds;         // Orbit duration
```

### Projectile
```csharp
public float lifetime;  // Auto-destroy after X seconds
```

---

## Summary

**You have**:
- ✅ 5 functional C# scripts ready to use
- ✅ Automated NASA texture importer
- ✅ Package builder for sharing
- ✅ Complete solar system data

**You need to**:
- ⬜ Run Planet Asset Importer once
- ⬜ Create or open a scene
- ⬜ Drag prefabs into scene
- ⬜ Press Play and test!

**Time investment**:
- Setup: 15 minutes
- Learning basics: 1-2 hours
- Building first scene: 30 minutes
- Having fun: Priceless! 🚀

**Remember**: Everything is already coded and working. You're assembling pieces, not building from scratch!

---

**Ready to start?** Open Unity, run the Planet Asset Importer, and explore DemoScene! 🎮
