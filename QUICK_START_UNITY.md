# Quick Start: Unity Planet Assets Setup

This is a condensed checklist for setting up realistic planet assets in the SpaceForce Unity project.

## Prerequisites (Install on Your Machine)

- [ ] **Git** - Version control
- [ ] **Git LFS** - Large file storage (`git lfs install`)
- [ ] **Unity 2023.4 LTS** - Game engine
- [ ] **(Optional)** `curl` and ImageMagick for manual shell script
- [ ] **GitHub Account** - With LFS enabled

## Setup Steps (Do These In Order)

### 1. Clone Repo & Create Feature Branch
```bash
git clone https://github.com/adamolson11/spaceForce.git
cd spaceForce
git checkout -b add/realistic-planet-assets
```

### 2. Ensure Git LFS is Active
```bash
git lfs install
```

### 3. Add Unity Editor Tools (One-Time)
Editor tools are already included in this repo:
- `Assets/Editor/PlanetAssetImporter.cs` ✓
- `Assets/Editor/PackageBuilder.cs` ✓

Commit them if not already in repo:
```bash
git add Assets/Editor/PlanetAssetImporter.cs Assets/Editor/PackageBuilder.cs
git commit -m "Add importer & package-builder editor tools"
```

### 4. Run Importer in Unity (Recommended Method)

1. **Open Unity 2023.4 LTS** pointing at the `spaceForce` project
2. **Set up URP**:
   - Edit → Project Settings → Graphics
   - Create URP asset: Right-click in Project → Create → Rendering → URP Asset
   - Assign to Scriptable Render Pipeline Settings
3. **Run Importer**:
   - Window → Planet Asset Importer → Open
   - Click: **Download Textures & Create Prefabs**
4. **Wait** until "Done" dialog appears (~2-5 minutes)

**What this creates:**
- Downloads 2K NASA textures
- Creates 2048/1024/512 resolution variants
- Generates Saturn rings
- Creates URP materials
- Builds planet prefabs
- Creates `DemoScene.unity`

### 5. Verify Assets Created
Check these folders:
```
Assets/Graphics/
├── Planets/       (textures in multiple resolutions)
├── Materials/     (URP materials)
├── Prefabs/       (planet prefabs)
└── Scenes/        (DemoScene.unity)
```

### 6. Test Demo Scene
1. Open `Assets/Graphics/Scenes/DemoScene.unity`
2. Press **Play** in Unity
3. Should see solar system with realistic textures

### 7. Commit & Push
```bash
git add Assets/Graphics/
git commit -m "Add realistic planet textures and prefabs from NASA"
git push origin add/realistic-planet-assets
```

### 8. Create Pull Request
1. Go to GitHub repo
2. Click "Compare & pull request"
3. Add description of changes
4. Submit PR for review

## Alternative: Manual Shell Script Method

If Unity importer doesn't work:

```bash
cd Assets
chmod +x download_assets.sh
./download_assets.sh
```

Then manually create materials and prefabs in Unity.

## Troubleshooting

### Git LFS not working?
```bash
git lfs fetch --all
git lfs pull
```

### Materials appear pink/magenta?
1. Check URP asset assigned in Project Settings → Graphics
2. Right-click materials → Reimport
3. Verify shader: Universal Render Pipeline/Lit

### Importer menu not appearing?
1. Check files exist: `Assets/Editor/PlanetAssetImporter.cs`
2. Check Unity Console for compilation errors
3. Restart Unity Editor

### Downloads failing?
- Check internet connection
- Try manual download from NASA websites
- Place textures in `Assets/Graphics/Planets/` manually

## Export Package (Share with Team)

After assets are created:

**Quick Export:**
```
Tools → SpaceForce → Build Planet Package (Quick)
```

**Or detailed options:**
```
Window → Package Builder → Open
Click "Build Planet Assets Package"
```

Package saved to: `Builds/PlanetAssets.unitypackage`

Team members import via: **Assets → Import Package → Custom Package**

## Files Created

| Path | Description |
|------|-------------|
| `UNITY_SETUP.md` | Detailed setup guide |
| `Assets/Editor/PlanetAssetImporter.cs` | One-click importer tool |
| `Assets/Editor/PackageBuilder.cs` | Package export tool |
| `Assets/Graphics/Planets/` | NASA textures (multiple resolutions) |
| `Assets/Graphics/Materials/` | URP materials |
| `Assets/Graphics/Prefabs/` | Planet prefabs |
| `Assets/Graphics/Scenes/DemoScene.unity` | Demo solar system |

## Resources

- **Detailed Guide**: `UNITY_SETUP.md`
- **Asset Info**: `Assets/ASSETS.md`
- **AI Agent Guide**: `.github/copilot-instructions.md`
- **NASA Textures**: https://solarsystem.nasa.gov/resources/
- **Unity URP Docs**: https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@latest

## Next Steps

After setup complete:
1. ✓ Explore demo scene
2. ✓ Use prefabs in your own scenes
3. ✓ Customize materials (add normal maps, etc.)
4. ✓ Add ship controller: `Assets/Scripts/ShipController.cs`
5. ✓ Integrate with quiz system

---

**Need Help?** Check `UNITY_SETUP.md` for detailed troubleshooting or create a GitHub issue.
