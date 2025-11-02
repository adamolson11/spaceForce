// Enhanced three.js 3D space game prototype
(() => {
  const container = document.getElementById('canvas-container');

  const scene = new THREE.Scene();
  
  // Game state
  let score = 0;
  let lives = 3;
  let gameOver = false;

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

  // Enemies with sprite support
  const enemies = [];
  const enemyTextures = {};
  
  // Load enemy textures
  loader.load('../beetlemorph.png', (tex) => {
    enemyTextures.beetlemorph = tex;
  });
  loader.load('../rhinomorph.png', (tex) => {
    enemyTextures.rhinomorph = tex;
  });
  loader.load('../boss.png', (tex) => {
    enemyTextures.boss = tex;
  });
  
  function spawnEnemy(x = 0, y = 180, type = 'basic') {
    const enemySize = type === 'boss' ? 150 : 80;
    const geo = new THREE.PlaneGeometry(enemySize, enemySize);
    let mat;
    
    if (type === 'beetlemorph' && enemyTextures.beetlemorph) {
      mat = new THREE.MeshBasicMaterial({ map: enemyTextures.beetlemorph, transparent: true });
    } else if (type === 'rhinomorph' && enemyTextures.rhinomorph) {
      mat = new THREE.MeshBasicMaterial({ map: enemyTextures.rhinomorph, transparent: true });
    } else if (type === 'boss' && enemyTextures.boss) {
      mat = new THREE.MeshBasicMaterial({ map: enemyTextures.boss, transparent: true });
    } else {
      // Fallback colors
      const color = type === 'boss' ? 0xff0000 : (type === 'rhinomorph' ? 0xff9900 : 0xff6666);
      mat = new THREE.MeshBasicMaterial({ color: color });
    }
    
    const m = new THREE.Mesh(geo, mat);
    m.position.set(x, y, 0);
    m.userData.vy = type === 'boss' ? -0.3 : -0.6;
    m.userData.type = type;
    m.userData.health = type === 'boss' ? 5 : (type === 'rhinomorph' ? 3 : 1);
    scene.add(m);
    enemies.push(m);
  }
  
  // Spawn initial enemies with variety
  spawnEnemy(-120, 200, 'beetlemorph');
  spawnEnemy(60, 180, 'rhinomorph');
  
  // Spawn new enemies periodically
  setInterval(() => {
    if (gameOver) return;
    const types = ['beetlemorph', 'rhinomorph'];
    const type = types[Math.floor(Math.random() * types.length)];
    const x = (Math.random() - 0.5) * 300;
    spawnEnemy(x, 280, type);
  }, 2000);

  // Bullets and particles
  const bullets = [];
  const particles = [];
  
  // Create explosion particles
  function createExplosion(x, y) {
    for (let i = 0; i < 15; i++) {
      const size = Math.random() * 8 + 4;
      const geo = new THREE.PlaneGeometry(size, size);
      const color = new THREE.Color().setHSL(Math.random() * 0.1 + 0.05, 1, 0.6); // Orange/yellow
      const mat = new THREE.MeshBasicMaterial({ color: color, transparent: true, opacity: 1 });
      const p = new THREE.Mesh(geo, mat);
      p.position.set(x, y, 0);
      p.userData.vx = (Math.random() - 0.5) * 4;
      p.userData.vy = (Math.random() - 0.5) * 4;
      p.userData.life = 1.0;
      scene.add(p);
      particles.push(p);
    }
  }

  // pointer move -> move player X
  container.addEventListener('mousemove', (e) => {
    if (!player) return;
    const rect = container.getBoundingClientRect();
    const xN = ((e.clientX - rect.left) / rect.width) * 2 - 1;
    const worldX = xN * (viewSize * aspect) / 2;
    player.position.x = worldX;
  });

  // Shooting with auto-fire
  let lastShot = 0;
  const shootCooldown = 200; // ms
  
  container.addEventListener('click', shootBullet);
  
  function shootBullet() {
    if (!player || gameOver) return;
    const now = Date.now();
    if (now - lastShot < shootCooldown) return;
    lastShot = now;
    
    // Create golden laser bullet with glow
    const bulletGeo = new THREE.PlaneGeometry(6, 24);
    const bulletMat = new THREE.MeshBasicMaterial({ 
      color: 0xffdd00,
      transparent: true,
      opacity: 0.9
    });
    const bullet = new THREE.Mesh(bulletGeo, bulletMat);
    bullet.position.set(player.position.x, player.position.y + 60, 0);
    bullet.userData.vy = 10;
    scene.add(bullet);
    bullets.push(bullet);
  }

  function update() {
    if (gameOver) return;
    
    // update bullets
    for (let i = bullets.length - 1; i >= 0; i--) {
      const b = bullets[i];
      b.position.y += b.userData.vy;
      if (b.position.y > viewSize / 2 + 50) {
        scene.remove(b);
        bullets.splice(i, 1);
      }
    }

    // update particles
    for (let i = particles.length - 1; i >= 0; i--) {
      const p = particles[i];
      p.position.x += p.userData.vx;
      p.position.y += p.userData.vy;
      p.userData.life -= 0.02;
      p.material.opacity = p.userData.life;
      
      if (p.userData.life <= 0) {
        scene.remove(p);
        particles.splice(i, 1);
      }
    }

    // update enemies
    for (let i = enemies.length - 1; i >= 0; i--) {
      const e = enemies[i];
      e.position.y += e.userData.vy;
      
      // Check collision with player
      if (player) {
        const dx = e.position.x - player.position.x;
        const dy = e.position.y - player.position.y;
        const dist2 = dx*dx + dy*dy;
        if (dist2 < 50*50) {
          createExplosion(e.position.x, e.position.y);
          scene.remove(e);
          enemies.splice(i, 1);
          lives--;
          updateHUD();
          if (lives <= 0) {
            gameOver = true;
            showGameOver();
          }
          continue;
        }
      }
      
      // Remove enemies that are off screen (player loses if enemies get through)
      if (e.position.y < -viewSize / 2 - 100) {
        scene.remove(e);
        enemies.splice(i, 1);
      }
    }

    // Collision: bullet -> enemy
    for (let i = bullets.length - 1; i >= 0; i--) {
      const b = bullets[i];
      if (!bullets[i]) continue; // Safety check
      
      for (let j = enemies.length - 1; j >= 0; j--) {
        const e = enemies[j];
        if (!enemies[j]) continue; // Safety check
        
        const dx = b.position.x - e.position.x;
        const dy = b.position.y - e.position.y;
        const dist2 = dx*dx + dy*dy;
        const r = 40;
        
        if (dist2 < r*r) {
          scene.remove(b); 
          bullets.splice(i, 1);
          
          e.userData.health--;
          if (e.userData.health <= 0) {
            createExplosion(e.position.x, e.position.y);
            scene.remove(e); 
            enemies.splice(j, 1);
            
            // Update score based on enemy type
            const points = e.userData.type === 'boss' ? 50 : (e.userData.type === 'rhinomorph' ? 10 : 5);
            score += points;
            updateHUD();
          }
          break;
        }
      }
    }
  }
  
  // HUD management
  const hudElement = document.querySelector('.hud');
  function updateHUD() {
    hudElement.innerHTML = `
      <div style="font-size: 20px; font-weight: bold;">
        Score: ${score} | Lives: ${'❤️'.repeat(lives)} | ${gameOver ? 'GAME OVER!' : 'Click to shoot'}
      </div>
    `;
  }
  
  function showGameOver() {
    hudElement.innerHTML = `
      <div style="font-size: 28px; font-weight: bold; color: #ff4444;">
        GAME OVER!<br>
        Final Score: ${score}<br>
        <span style="font-size: 18px;">Refresh to play again</span>
      </div>
    `;
  }
  
  updateHUD();

  function animate() {
    requestAnimationFrame(animate);
    update();
    renderer.render(scene, camera);
  }

  animate();
})();