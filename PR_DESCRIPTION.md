# Add realistic planet assets (2k textures, prefabs, DemoScene)

## Summary
- Merge branch: add/realistic-planet-assets → main
- Purpose: Add realistic planet textures (2k albedo maps and 1024/512 variants), Saturn ring texture, Europa & Titan moon textures and prefabs, URP materials, planet prefabs, a placeholder realistic ship prefab, projectile prefab, ObjectPool prefab, and a DemoScene demonstrating the setup.

## Files and folders expected (verify they exist in the branch)
- Assets/Graphics/Planets/ (sun_2048.png, mercury_2048.png, venus_2048.png, earth_2048.png, moon_2048.png, mars_2048.png, jupiter_2048.png, saturn_2048.png, saturn_rings_2048.png, uranus_2048.png, neptune_2048.png, europa_2048.png, titan_2048.png and corresponding _1024/_512 variants)
- Assets/Graphics/Ship/ (realistic ship model and textures or placeholder Ship.prefab)
- Assets/Materials/ (URP Lit materials for Sun and planets, Saturn_Ring_Mat.mat)
- Assets/Prefabs/ (Planet_{name}.prefab, Saturn_Rings.prefab, Ship.prefab, Projectile.prefab, ObjectPool.prefab)
- Assets/Scenes/DemoScene.unity
- Assets/Editor/PlanetAssetImporter.cs (editor importer)
- Assets/Editor/PackageBuilder.cs (package exporter)
- .gitattributes (Git LFS tracking for Assets/Graphics)

## Testing instructions
1. Pull branch: `git fetch origin && git checkout add/realistic-planet-assets`
2. Ensure Git LFS is installed: `git lfs install`
3. Open project in Unity 2023.4 LTS and assign a URP pipeline asset (Project Settings → Graphics)
4. Window → Planet Asset Importer → Download Textures & Create Prefabs (wait for Done)
5. Open Assets/Scenes/DemoScene.unity and press Play — verify the Sun and planets render with textures and Saturn rings display and Europa/Titan exist
6. Optional: Window → Package Builder → Export Planet Assets to generate Packages/spaceforce_planet_assets.unitypackage

## Attribution and licensing
- Planet textures: SolarSystemScope / NASA (public domain) — include source links in ASSETS.md
- Ship models: list CC0/CC-BY sources in ASSETS.md
- Note: Large binaries are tracked via Git LFS; ensure repo has LFS quota or attach unitypackage as PR asset

## Checklist for reviewers
- [ ] Assets exist under Assets/Graphics/Planets and are tracked by LFS
- [ ] URP materials use Universal Render Pipeline/Lit
- [ ] DemoScene opens and renders correctly in Unity 2023.4 LTS
- [ ] ASSETS.md updated with exact source links and attribution
- [ ] Package exported (optional) and attached to PR if LFS is not available
