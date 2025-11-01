// Minimal three.js prototype mapping your 2D sprites to a 3D scene
(() => {
  const container = document.getElementById('canvas-container');

  const scene = new THREE.Scene();

  // Camera - use Orthographic to keep a consistent 2D-like layout
  let w = container.clientWidth;
  let h = container.clientHeight;
  let aspect = w / h;
  const viewSize = 600;
  const camera = new THREE.OrthographicCamera(
    -viewSize * aspect / 2,
    viewSize * aspect / 2,
    viewSize / 2,
    -viewSize / 2,
    0.1,
    2000
  );
  camera.position.set(0, 0, 1000);

  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
  renderer.setSize(w, h);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  container.appendChild(renderer.domElement);

  window.addEventListener('resize', onResize);
  function onResize() {
    w = container.clientWidth;
    h = container.clientHeight;
    aspect = w / h;
    renderer.setSize(w, h);
    camera.left = -viewSize * aspect / 2;
    camera.right = viewSize * aspect / 2;
    camera.top = viewSize / 2;
    camera.bottom = -viewSize / 2;
    camera.updateProjectionMatrix();
  }

  // Ambient light (useful once we move to true 3D objects)
  const ambient = new THREE.AmbientLight(0xffffff, 0.9);
  scene.add(ambient);

  // Texture loader (re-uses assets in your repo root)
  const loader = new THREE.TextureLoader();
  loader.setCrossOrigin('');

  // Background plane (PlayPageBackground.png expected at repo root)
  loader.load('PlayPageBackground.png', (bgTex) => {
    const bgGeo = new THREE.PlaneGeometry(viewSize * aspect, viewSize);
    const bgMat = new THREE.MeshBasicMaterial({ map: bgTex });
    const bg = new THREE.Mesh(bgGeo, bgMat);
    bg.position.set(0, 0, -500); // behind everything
    scene.add(bg);
  }, undefined, () => {
    // fallback background color if texture missing
    scene.background = new THREE.Color(0x001020);
  });

  // Player as a textured plane
  const playerSize = 120;
  let player;
  loader.load('player.png', (tex) => {
    const geo = new THREE.PlaneGeometry(playerSize, playerSize);
    const mat = new THREE.MeshBasicMaterial({ map: tex, transparent: true });
    player = new THREE.Mesh(geo, mat);
    player.position.set(0, -120, 0);
    scene.add(player);
  }, undefined, () => {
    // fallback simple shape if texture missing
    const geo = new THREE.PlaneGeometry(playerSize, playerSize);
    const mat = new THREE.MeshBasicMaterial({ color: 0x66ccff });
    player = new THREE.Mesh(geo, mat);
    player.position.set(0, -120, 0);
    scene.add(player);
  });

  // Simple enemy for demo
  const enemies = [];
  function spawnEnemy(x = 0, y = 180) {
    const geo = new THREE.PlaneGeometry(100, 100);
    const mat = new THREE.MeshBasicMaterial({ color: 0xff6666 });
    const m = new THREE.Mesh(geo, mat);
    m.position.set(x, y, 0);
    m.userData.vy = -0.6;
    scene.add(m);
    enemies.push(m);
  }
  spawnEnemy(-120);
  spawnEnemy(60);

  // Bullets
  const bullets = [];

  // pointer move -> move player X
  container.addEventListener('mousemove', (e) => {
    if (!player) return;
    const rect = container.getBoundingClientRect();
    const xN = ((e.clientX - rect.left) / rect.width) * 2 - 1;
    const worldX = xN * (viewSize * aspect) / 2;
    player.position.x = worldX;
  });

  container.addEventListener('click', () => {
    if (!player) return;
    const bulletGeo = new THREE.PlaneGeometry(8, 20);
    const bulletMat = new THREE.MeshBasicMaterial({ color: 0xffcc00 });
    const bullet = new THREE.Mesh(bulletGeo, bulletMat);
    bullet.position.set(player.position.x, player.position.y + 60, 0);
    bullet.userData.vy = 8;
    scene.add(bullet);
    bullets.push(bullet);
  });

  function update() {
    // update bullets
    for (let i = bullets.length - 1; i >= 0; i--) {
      const b = bullets[i];
      b.position.y += b.userData.vy;
      if (b.position.y > viewSize / 2 + 50) {
        scene.remove(b);
        bullets.splice(i, 1);
      }
    }

    // update enemies
    for (let i = enemies.length - 1; i >= 0; i--) {
      const e = enemies[i];
      e.position.y += e.userData.vy;
      if (e.position.y < -viewSize / 2 - 100) {
        scene.remove(e);
        enemies.splice(i, 1);
      }
    }

    // very simple collision: bullet -> enemy
    for (let i = bullets.length - 1; i >= 0; i--) {
      const b = bullets[i];
      for (let j = enemies.length - 1; j >= 0; j--) {
        const e = enemies[j];
        const dx = b.position.x - e.position.x;
        const dy = b.position.y - e.position.y;
        const dist2 = dx*dx + dy*dy;
        const r = 40;
        if (dist2 < r*r) {
          scene.remove(b); bullets.splice(i,1);
          scene.remove(e); enemies.splice(j,1);
          // spawn a replacement enemy after a short delay
          setTimeout(() => spawnEnemy((Math.random()-0.5)*300, 260), 600);
          break;
        }
      }
    }
  }

  function animate() {
    requestAnimationFrame(animate);
    update();
    renderer.render(scene, camera);
  }

  animate();
})();