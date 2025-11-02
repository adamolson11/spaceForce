# ASSETS and SOURCES (add/realistic-planet-textures)

This file lists the planned asset layout, recommended sources (NASA public domain textures), and notes for integration.

## Quick Start

**NEW: Automated Setup!** Use the Unity Editor importer tool for one-click asset setup:

1. Open project in Unity 2023.4 LTS
2. **Window → Planet Asset Importer → Open**
3. Click "Download Textures & Create Prefabs"
4. Done! All assets created automatically.

See **[UNITY_SETUP.md](../UNITY_SETUP.md)** for detailed step-by-step instructions.

## Recommended Unity version and pipeline
- Unity 2023.4 LTS (recommended) with Universal Render Pipeline (URP).
- If you prefer 2022.3 LTS, tell me and I will use that instead.

Planned asset layout (place under Assets/Graphics/)
- Graphics/
  - Planets/
    - sun_albedo.png
    - sun_emissive.png (optional combined map)
    - mercury_albedo.png
    - venus_albedo.png
    - earth_albedo.png
    - earth_normal.png (optional)
    - moon_albedo.png
    - mars_albedo.png
    - jupiter_albedo.png
    - saturn_albedo.png
    - saturn_rings.png (alpha PNG)
    - uranus_albedo.png
    - neptune_albedo.png
  - Ship/
    - ship_model.fbx or ship_model.gltf
    - ship_albedo.png
    - ship_normal.png (optional)
  - Projectiles/
    - projectile_albedo.png
  - Materials/
    - Planet_{name}.mat
    - Sun_Emissive.mat
  - Prefabs/
    - Planet_{name}.prefab
    - Saturn_Ring.prefab
    - Ship.prefab
    - Projectile.prefab

Recommended sources (public-domain / permissive)
- NASA planetary textures (public domain): https://visibleearth.nasa.gov/ or https://svs.gsfc.nasa.gov/ and planetary texture downloads linked from NASA/USGS. NASA imagery is public domain; still include a short credit line in any public project.
- Low-mid poly ship models:
  - OpenGameArt.org (filter for CC0/CC-BY)
  - Sketchfab (check license)
  - Kenney.nl for complementary assets
- For rings (Saturn): use a separate alpha PNG mapped to a flat ring mesh.

## Editor Tools

Two Unity Editor tools are provided in `Assets/Editor/`:

### PlanetAssetImporter.cs
Automated asset importer that:
- Downloads NASA textures via Unity Web Request
- Creates multiple resolution variants (2048, 1024, 512)
- Generates URP materials for each planet
- Creates planet prefabs with proper materials
- Builds Saturn rings with transparency
- Creates demo scene with full solar system

**Usage**: Window → Planet Asset Importer → Open

### PackageBuilder.cs
Package export tool that:
- Bundles all planet assets into .unitypackage
- Configurable asset inclusion (textures, materials, prefabs, scenes, scripts)
- Quick export via Tools → SpaceForce → Build Planet Package (Quick)
- Outputs to `Builds/` folder for easy sharing

**Usage**: Window → Package Builder → Open

## Integration notes
- Use sphere meshes (Unity built-in Sphere or custom low-poly sphere for LOD control).
- For Sun: use an emissive URP material + bloom post-processing to get glow.
- For Saturn rings: tilt the ring mesh and place it slightly above the planet surface to avoid z-fighting.
- Performance: create lower-resolution mipmap variants and set platform-specific texture compression (ASTC/ETC for mobile, BCn for desktop).
- Physics vs visual scale: do not use real solar system scale. Use separate scales: visualScale for distances/positions and physicsScale for integrator constants.

## Licensing and credits
- NASA: public domain (credit NASA in documentation).
- Any third-party 3D models will be listed here with attribution if required.

## Manual Alternative

For manual setup without editor tools, use the shell script:
```bash
cd Assets
chmod +x download_assets.sh
./download_assets.sh
```

Then manually create materials, prefabs, and scenes in Unity.
