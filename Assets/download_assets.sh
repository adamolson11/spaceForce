#!/usr/bin/env bash
set -e
BASE_DIR="Assets/Graphics/Planets"
mkdir -p "$BASE_DIR"

echo "Downloading 2k planet albedo maps (SolarSystemScope)..."
curl -L -o "$BASE_DIR/2k_sun.jpg" https://www.solarsystemscope.com/textures/download/2k_sun.jpg
curl -L -o "$BASE_DIR/2k_mercury.jpg" https://www.solarsystemscope.com/textures/download/2k_mercury.jpg
curl -L -o "$BASE_DIR/2k_venus.jpg" https://www.solarsystemscope.com/textures/download/2k_venus_surface.jpg
curl -L -o "$BASE_DIR/2k_earth.jpg" https://www.solarsystemscope.com/textures/download/2k_earth_daymap.jpg
curl -L -o "$BASE_DIR/2k_moon.jpg" https://www.solarsystemscope.com/textures/download/2k_moon.jpg
curl -L -o "$BASE_DIR/2k_mars.jpg" https://www.solarsystemscope.com/textures/download/2k_mars.jpg
curl -L -o "$BASE_DIR/2k_jupiter.jpg" https://www.solarsystemscope.com/textures/download/2k_jupiter.jpg
curl -L -o "$BASE_DIR/2k_saturn.jpg" https://www.solarsystemscope.com/textures/download/2k_saturn.jpg
curl -L -o "$BASE_DIR/2k_uranus.jpg" https://www.solarsystemscope.com/textures/download/2k_uranus.jpg
curl -L -o "$BASE_DIR/2k_neptune.jpg" https://www.solarsystemscope.com/textures/download/2k_neptune.jpg

echo "Creating mip variants (1024, 512)..."
for f in "$BASE_DIR"/2k_*.jpg; do
  base=$(basename "$f" .jpg)
  convert "$f" -resize 2048x1024 "$BASE_DIR/${base}_2048.png"
  convert "$f" -resize 1024x512 "$BASE_DIR/${base}_1024.png"
  convert "$f" -resize 512x256 "$BASE_DIR/${base}_512.png"
done

cat > "$BASE_DIR/README_DOWNLOAD.txt" <<EOT
Downloaded from SolarSystemScope (publicly available textures). Review ASSETS.md for full attributions.
Note: Saturn rings, Europa and Titan textures are not included by default. Add them manually into this folder if desired.
EOT

echo "Done."