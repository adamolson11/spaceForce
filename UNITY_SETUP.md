# Unity Setup Guide - Realistic Planet Assets

This guide walks you through setting up the SpaceForce Unity project with realistic planet textures from NASA.

## Prerequisites (Install on Your Machine)

1. **Git** - Version control system
2. **Git LFS** - Large File Storage for textures
   ```bash
   git lfs install
   ```
3. **Unity 2023.4 LTS** - Download from [Unity Hub](https://unity.com/download)
4. **(Optional)** For manual shell script: `curl` and `ImageMagick` (`convert` command)
5. **GitHub Account** - With LFS enabled for the repo

## Quick Start (Recommended Method)

### Step 1: Clone Repository & Create Feature Branch
```bash
git clone https://github.com/adamolson11/spaceForce.git
cd spaceForce
git checkout -b add/realistic-planet-assets
```

### Step 2: Ensure Git LFS is Active
```bash
git lfs install
```

### Step 3: Open Project in Unity
1. Open **Unity Hub**
2. Click **Add** → Select `spaceForce` folder
3. Open project with **Unity 2023.4 LTS**

### Step 4: Set Up URP (Universal Render Pipeline)
1. In Unity menu: **Edit → Project Settings → Graphics**
2. If no URP asset exists:
   - Right-click in Project window: **Create → Rendering → URP Asset (with Universal Renderer)**
   - Assign the created asset to **Scriptable Render Pipeline Settings**

### Step 5: Run the Planet Asset Importer (One Click!)
1. In Unity menu: **Window → Planet Asset Importer → Open**
2. Click: **Download Textures & Create Prefabs**
3. Wait for the process to complete (~2-5 minutes depending on internet speed)

**What this does:**
- Downloads 2K NASA textures for all planets
- Creates 2048/1024/512 resolution variants
- Generates Saturn ring texture
- Creates materials with proper URP shaders
- Builds planet prefabs
- Creates `DemoScene.unity` with solar system layout

### Step 6: Verify Assets
Check `Assets/Graphics/` for:
- `Planets/` - All planet textures (multiple resolutions)
- `Materials/` - Planet materials with URP shaders
- `Prefabs/` - Planet prefabs ready to use
- `Scenes/DemoScene.unity` - Demo solar system scene

### Step 7: Test the Demo Scene
1. Open `Assets/Graphics/Scenes/DemoScene.unity`
2. Press **Play** in Unity
3. You should see a 3D solar system with realistic textures

### Step 8: Commit Your Work
```bash
git add Assets/Graphics/
git commit -m "Add realistic planet textures and prefabs"
git push origin add/realistic-planet-assets
```

## Alternative Method: Manual Shell Script

If you prefer manual control or the editor tool doesn't work:

### Run the Download Script
```bash
cd Assets
chmod +x download_assets.sh
./download_assets.sh
```

This script:
- Downloads NASA textures using `curl`
- Creates resolution variants using ImageMagick
- Organizes files in proper folder structure

### Manual Unity Setup
1. Open Unity project
2. Create materials manually in `Assets/Graphics/Materials/`
3. Assign textures to materials
4. Create sphere prefabs and assign materials
5. Build demo scene

## Troubleshooting

### Git LFS Issues
If textures aren't downloading:
```bash
git lfs fetch --all
git lfs pull
```

### Unity Version Mismatch
If Unity version doesn't match:
- Install Unity 2023.4 LTS specifically
- Or update project files to your Unity version (may require testing)

### URP Not Working
If materials appear pink/magenta:
1. Check that URP asset is assigned in **Project Settings → Graphics**
2. Reimport materials: Right-click → **Reimport**
3. Ensure shaders are set to **Universal Render Pipeline/Lit**

### Download Failures
If NASA texture downloads fail:
- Check internet connection
- Try manual download from NASA websites
- Place textures in `Assets/Graphics/Planets/` manually

### Missing Editor Tools
If **Window → Planet Asset Importer** doesn't appear:
1. Ensure files exist: `Assets/Editor/PlanetAssetImporter.cs` and `Assets/Editor/PackageBuilder.cs`
2. Check for compilation errors in Unity Console
3. Restart Unity Editor

## Asset Sources

All textures from NASA (Public Domain):
- **Planets**: NASA Visible Earth, NASA SVS
- **Sun**: NASA Solar Dynamics Observatory
- Credit line required in public distributions: "Planetary textures courtesy of NASA"

## Next Steps

After setup:
1. Explore `DemoScene.unity` to see planet layout
2. Use planet prefabs in your own scenes
3. Customize materials (add normal maps, emission, etc.)
4. Adjust planet scales for gameplay vs. realism
5. Add ship controller from `Assets/Scripts/ShipController.cs`

## Export as Unity Package

To share assets with team:
1. In Unity: **Window → Package Builder → Open**
2. Click: **Build Planet Assets Package**
3. Package saved to `Builds/PlanetAssets.unitypackage`
4. Others can import via **Assets → Import Package → Custom Package**

## File Structure After Setup

```
Assets/
├── Editor/
│   ├── PlanetAssetImporter.cs    # One-click importer tool
│   └── PackageBuilder.cs          # Package export tool
├── Graphics/
│   ├── Planets/
│   │   ├── sun_2048.png
│   │   ├── sun_1024.png
│   │   ├── mercury_2048.png
│   │   ├── [all planets, 3 resolutions each]
│   │   └── saturn_rings_2048.png
│   ├── Materials/
│   │   ├── Sun_Emissive.mat
│   │   ├── Planet_Mercury.mat
│   │   └── [materials for each planet]
│   ├── Prefabs/
│   │   ├── Sun.prefab
│   │   ├── Planet_Mercury.prefab
│   │   └── [prefabs for each planet]
│   └── Scenes/
│       └── DemoScene.unity         # Demo solar system
├── Scripts/
│   ├── ShipController.cs
│   ├── PlanetController.cs
│   └── [other gameplay scripts]
└── ASSETS.md                       # Asset documentation
```

## Development Workflow

### Adding New Planets/Celestial Bodies
1. Download texture from NASA
2. Place in `Assets/Graphics/Planets/`
3. Create material using URP/Lit shader
4. Create prefab with sphere mesh
5. Add to demo scene

### Texture Resolution Guidelines
- **Desktop/Console**: Use 2048px textures
- **Mobile/VR**: Use 1024px or 512px textures
- **Performance testing**: Start with 512px, scale up as needed

### Material Settings (URP)
- **Shader**: Universal Render Pipeline/Lit
- **Workflow**: Metallic
- **Surface Type**: Opaque (except rings - use Transparent)
- **Emission**: Enabled for Sun only

## Additional Resources

- [NASA Visible Earth](https://visibleearth.nasa.gov/)
- [NASA SVS](https://svs.gsfc.nasa.gov/)
- [Unity URP Documentation](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@latest)
- [SpaceForce README](README.md)
- [Assets Documentation](Assets/ASSETS.md)

## Support

For issues or questions:
1. Check `Assets/ASSETS.md` for asset-specific info
2. Review Unity Console for errors
3. Create GitHub issue with details
4. Include Unity version and error logs
