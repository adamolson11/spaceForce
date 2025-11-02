# Unity Steps - Execute These in Unity Editor

**Branch**: `add/realistic-planet-assets`  
**Goal**: Generate planet assets and export UnityPackage

---

## Step 1: Open Unity Project

1. **Launch Unity Hub**
2. **Open Project**: Select the `spaceForce` folder
3. **Unity Version**: Ensure you're using **Unity 2023.4 LTS**
   - If not installed, install it via Unity Hub

---

## Step 2: Set Up URP (Universal Render Pipeline)

**If URP is already configured, skip to Step 3.**

1. **Edit → Project Settings**
2. Click **Graphics** in left sidebar
3. **Scriptable Render Pipeline Settings**:
   - If empty, create URP asset:
     - Right-click in Project window
     - **Create → Rendering → URP Asset (with Universal Renderer)**
     - Drag created asset to the field
4. **Close** Project Settings

---

## Step 3: Download & Generate Assets (ONE CLICK!)

1. **Unity Menu**: `Window → Planet Asset Importer → Open`
2. **Click**: `Download Textures & Create Prefabs` (big button)
3. **Wait**: Progress bar will show download status (~2-5 minutes)
   - Downloads NASA textures for:
     - Sun, Mercury, Venus, Earth, Mars
     - Jupiter, **Europa** (Jupiter's moon)
     - Saturn, **Titan** (Saturn's moon)
     - Uranus, Neptune
   - Creates Saturn rings
   - Generates materials & prefabs
   - Builds demo scene
4. **Wait for "Done" Dialog** - Don't close Unity until complete!

---

## Step 4: Verify Assets Created

Check these folders in Project window:

```
Assets/Graphics/
├── Planets/     ✓ (11 celestial bodies × 3 resolutions each)
├── Materials/   ✓ (URP materials for each body)
├── Prefabs/     ✓ (Planet prefabs with materials)
└── Scenes/      ✓ (DemoScene.unity)
```

**Quick Test**:
- Open `Assets/Graphics/Scenes/DemoScene.unity`
- Press **Play** button
- Should see solar system with realistic textures

---

## Step 5: Export UnityPackage

1. **Unity Menu**: `Window → Package Builder → Open`
2. **Verify Settings**:
   - ✓ Include Textures (Graphics/Planets/)
   - ✓ Include Materials (Graphics/Materials/)
   - ✓ Include Prefabs (Graphics/Prefabs/)
   - ✓ Include Scenes (Graphics/Scenes/)
   - ✓ Include Scripts (Scripts/)
3. **Package Name**: Should show `spaceforce_planet_assets`
4. **Output Folder**: Should show `Packages`
5. **Click**: `Build Planet Assets Package` (big button)
6. **Unity Export Dialog**: Click `Export` (keep all items selected)
7. **Success**: Package created at `Packages/spaceforce_planet_assets.unitypackage`

---

## Step 6: Return to Terminal for Git Commands

**You're done in Unity!** Close the editor tools and return to your terminal.

The next steps are Git commands (already prepared in your terminal instructions).

---

## Troubleshooting

### Importer Fails to Download
- **Check internet connection**
- **Try again** - Click button again
- **Check Unity Console** (Window → General → Console) for errors
- **Manual fallback**: See `UNITY_SETUP.md` for manual download instructions

### Materials Appear Pink/Magenta
- **URP not set**: Go back to Step 2
- **Reimport**: Right-click materials → Reimport
- **Shader**: Check material uses "Universal Render Pipeline/Lit"

### Package Builder Can't Find Assets
- **Assets not created**: Go back to Step 3
- **Check folders exist**: Assets/Graphics/Planets, Materials, Prefabs, Scenes
- **Run importer first**: Must complete Step 3 before Step 5

### Unity Crashes or Freezes
- **Wait longer**: Downloads take 2-5 minutes
- **Check disk space**: Need ~50MB free
- **Restart Unity**: Close and reopen project, try again

---

## Expected File Sizes

- **Textures**: ~40-50 MB total (11 bodies × 3 resolutions)
- **UnityPackage**: ~35-45 MB compressed
- **Total Assets**: ~60-70 MB in project

---

## What Gets Created

| Asset Type | Count | Location |
|------------|-------|----------|
| Planet Textures | 33 files | Assets/Graphics/Planets/ |
| URP Materials | 12 materials | Assets/Graphics/Materials/ |
| Planet Prefabs | 12 prefabs | Assets/Graphics/Prefabs/ |
| Demo Scene | 1 scene | Assets/Graphics/Scenes/ |
| Saturn Rings | 1 texture | Assets/Graphics/Planets/ |

**Celestial Bodies**:
- Sun (emissive)
- Mercury, Venus, Earth, Mars
- Jupiter + Europa (moon)
- Saturn + Titan (moon) + Rings
- Uranus, Neptune

---

## Next: Git Commands

After Unity completes, run these in terminal:

```bash
git add Assets/Graphics Assets/Materials Assets/Prefabs Assets/Scenes
git add Assets/Editor
git commit -m "Add 2k planet textures, Saturn rings, Europa/Titan, ship & DemoScene (generated)"
git push --set-upstream origin add/realistic-planet-assets
```

Then create PR on GitHub and attach `Packages/spaceforce_planet_assets.unitypackage`.

---

**Need Help?** Check `UNITY_SETUP.md` for detailed troubleshooting or ask for assistance!
