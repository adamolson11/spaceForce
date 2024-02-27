class Player {
    constructor(game){
        this.game= game; 
        this.width= 140;
        this.height= 120;
        
        this.x = this.game.width * 0.5; 
        this.y = this.game.height- this.height; 
        this.speed = 5; 
        this.lives = 3; 
        this.maxLives = 10;
        this.image = document.getElementById('player'); 
        this.jets_image = document.getElementById('player_jets'); 
        this.frameX = 0; 
        this.jetsFrame = 1; 

    }
    draw(context){
        // context.fillRect(this.x, this.y, this.width, this.height); 
        // sprite frames
        if (this.game.keys.indexOf('1') > -1){
            this.frameX = 1;
        } else {
            this.frameX = 0; 
        }
        context.drawImage(this.jets_image, this.jetsFrame * this.width, 0, this.width, this.height, this.x, this.y, this.width, this.height); 
        context.drawImage(this.image, this.frameX* this.width, 0, this.width, this.height, this.x, this.y, this.width, this.height); 
      
    }
    update(){
        // horizontal movement 
        if (this.game.keys.indexOf('ArrowLeft') > -1){
         this.x -= this.speed;
         this.jetsFrame = 0; 
        }else  if 
        (this.game.keys.indexOf('ArrowRight') > -1) {this.x += this.speed;
            this.jetsFrame = 2; 
        } else {
            this.jetsFrame = 1;
        }
        //horizontal boundaries prevents from going outside of the box
        if (this.x < -this.width * 0.5) this.x = -this.width * 0.5;
        else if (this.x > this.game.width - this.width * 0.5) this.x = this.game.width -this.width *0.5;

    }
    shoot(){
        const projectile = this.game.getProjectile()
        if (projectile) projectile.start(this.x + this.width * 0.5, this.y); 


    }

    restart() {
        this.x = this.game.width * 0.5 - this.width * 0.5;
        this.y = this.game.height - this.height; 
        this.lives = 3; 
         
        
    }

}

class Projectile {
    constructor(){
        this.width = 3; 
        this.height = 40; 
        this.x = 0;  
        this.y = 0; 
        this.speed = 20 
        this.free = true; //object pool cleaning and garbage collection

    }
    draw(context){
        if (!this.free){
            context.save(); 
            context.fillStyle = 'gold'
            context.fillRect(this.x,this.y, this.width, this.height);  
            context.restore();   
        }
   
    }
    update(){
        if (!this.free){
            this.y -= this.speed; // part is like saying, "Move the spaceship up by a little bit."
                if(this.y < -this.height) this.reset() // like saying "reload! the array"
        }
    }
    start (x,y){
        this.x = x -this.width * 0.5; 
        this.y = y;
        this.free = false; 
    }

    reset(){
        this.free = true; 
    }

    
}

class Enemy {
    constructor(game, positionX, positionY){
        this.game = game; 
        this.width= this.game.enemySize; 
        this.height= this.game.enemySize; 
        this.x= 0; 
        this.y= 0; 
        this.positionX= positionX; 
        this.positionY= positionY; 
        this.markedForDeletion = false; 


    }
    draw(context){
       
        context.drawImage(this.image, this.frameX * this.width, this.frameY * this.height, this.width, this.height, this.x, this.y, this.width, this.height) 
    }
    update(x,y){
        this.x = x + this.positionX; 
        this.y = y + this.positionY; 
        //check for projectiles. 
        this.game.projectilesPool.forEach(projectile => {
           if ( !projectile.free && this.game.checkCollision(this,projectile) && this.lives >0) {
               this.hit(1);
                projectile.reset(); 
                
           }

           
        });
        if (this.lives < 1) {
            if (this.game.spriteUpdate) this.frameX++;
                if (this.frameX > this.maxFrame){
                    this.markedForDeletion = true;
                    if (!this.game.gameOver) this.game.score += this.maxLives;
                }


        }
        if (this.game.checkCollision(this, this.game.player) && this.lives > 0){
            // this.markedForDeletion = true; 
            // if (!this.game.gameOver && this.game.score > 0) this.game.score--;
            this.lives = 0;
            this.game.player.lives--; 
            // if (this.game.player.lives < 1) this.game.gameOver= true; 
        }
       //lose condition
        if (this.y +this.height > this.game.height || this.game.player.lives < 1) {
            this.game.gameOver = true;
            

        }
    }
    hit(damage){
        this.lives -= damage;

    }
}

class Beetlemorph extends Enemy {
    constructor(game, positionX, positionY) {
        super(game, positionX, positionY); 
        this.image = document.getElementById('beetlemorph')
        this.frameX = 0; // horizontal exploration around the beetlemorph spreadsheet
        this.maxFrame = 2;
        this.frameY = Math.floor(Math.random() * 4); //vertical exploration around the beetlemorph spreadsheet
        this.lives = 1; //says this lives 1 hit(damage)
        this.maxLives = this.lives; 
    }

}



class Wave {
    constructor(game){
        this.game = game; 
        this.width = this.game.columns * this.game.enemySize; 
        this.height= this.game.rows * this.game.enemySize; 
        this.x = this.game.width * 0.5 - this.width * 0.5; 
        this.y = -this.height;
        this.speedX = Math.random() < 0.5 ? -1 : 1; //ternary operator randomizes what direction the wave moves laterally
        this.speedY = 0; 
        this.enemies = []; 
        this.nextWaveTrigger = false;
        this.create(); 
     }
     render(context) {
        if (this.y <0) this.y += 5; 
        this.speedY = 0;
        this.x += this.speedX;
        if (this.x < 0 || this.x > this.game.width - this.width){
            this.speedX *= -1; 
            this.speedY = this.game.enemySize;
        }
            this.x += this.speedX;
            this.y += this.speedY;
            this.enemies.forEach(enemy => {
                enemy.update(this.x, this.y);
                enemy.draw(context); 

            })
            this.enemies = this.enemies.filter(object => !object.markedForDeletion);
     }
     create(){
            for (let y = 0; y < this.game.rows; y++){
                for (let x = 0; x < this.game.columns; x++) {
                    let enemyX = x * this.game.enemySize; 
                    let enemyY = y * this.game.enemySize; 
                    this.enemies.push(new Beetlemorph(this.game, enemyX, enemyY))

                } 

            }
        }
}



class Game { // like the brains of the whole thing
    constructor(canvas){//blueprint for canvas 
        this.canvas = canvas; //local instance of canvas limits it within the object
        this.width = this.canvas.width; //local instance of width and height
        this.height = this.canvas.height;
        this.keys = []; 
        this.player = new Player(this)
        

        this.projectilesPool = [];  
        this.numberOfProjectiles = 15; 
        this.createProjectiles(); 
        this.fired = false; //flags the keydown for projectile so that it stops from constant firing.
        this.columns = 1; 
        this.rows = 1; 
        this.enemySize = 80;

        this.waves = []; 

        this.waves.push(new Wave(this)); 
        this.waveCount = 1; 


        this.spriteUpdate = false; 
        this.spriteTimer = 0; 
        this.spriteInterval = 150;

        this.score = 0; 
        this.gameOver = false; 


        //event listeners for key board functions
        window.addEventListener('keydown', e => {
            if (e.key === '1' && !this.fired) this.player.shoot(); 
            this.fired = true;
            if (this.keys.indexOf(e.key) === -1) this.keys.push(e.key)//push method add the specified elements to the end of an array and returns the new length of the array.
           
            if (e.key === 'r' && this.gameOver) this.restart(); 
        })
        window.addEventListener('keyup', e => {
            this.fired = false; 
            const index = this.keys.indexOf(e.key);
            if (index > -1) {
                this.keys.splice(index, 1);
               
            }
        });
        
    }
    render(context, deltaTime){
        //Sprite timing is here... 
        if (this.spriteTimer> this.spriteInterval){
            this.spriteUpdate = true;
            this.spriteTimer= 0; 

        } else {
            this.spriteUpdate = false; 
            this.spriteTimer += deltaTime; 
        }

        this.drawStatusText(context)
        this.projectilesPool.forEach(projectile => {
            projectile.update(); 
            projectile.draw(context); 
        });
        this.player.draw(context); 
        this.player.update(); 
      
        this.waves.forEach(wave => {
            wave.render(context);
            if (wave.enemies.length < 1 && !wave.nextWaveTrigger && !this.gameOver) {
                this.newWave(); 
                this.waveCount++; 
                wave.nextWaveTrigger = true;
               if( this.player.lives< this.player.maxLives) this.player.lives++;
            }
        });
    }
    
    createProjectiles(){
            for (let i = 0; i < this.numberOfProjectiles; i++){
                this.projectilesPool.push(new Projectile()); // this is like putting the new bullet we made into our box of bullets

            }
    }
    getProjectile () {
            for (let i = 0; i < this.projectilesPool.length; i++){
                if (this.projectilesPool[i].free) return this.projectilesPool[i]; 
            }

    }
    // collision detection 
    checkCollision(a, b){
        return (
            a.x < b.x + b.width && 
            a.x + a.width > b.x &&
            a.y < b.y + b.height && 
            a.y + a.height > b.y
            )
        }
    drawStatusText(context) {
        context.save();
        context.shadowOffsetX = 2; 
        context.shadowOffsetY = 2; 
        context.shadowColor = 'black'; 
        context.fillText('Score: ' + this.score, 20, 40); 
        context.fillText('Wave: ' + this.waveCount, 20, 80); 
        
        for (let i = 0; i < this.player.maxLives; i++) {
            context.strokeRect(20 + 20 * i,100,5,20); 
        }



        for (let i = 0; i < this.player.lives; i++) {
            context.fillRect(20 + 20 * i,100,5,20); 
        }


        if (this.gameOver) {
            context.textAlign= 'center'; 
            context.font = '100px Impact'; 
            context.fillText("GAME OVER!", this.width * 0.5, this.height * 0.5); 
            context.font = '20px Impact'; 
            context.fillText("Press R to restart!", this.width * 0.5, this.height * 0.5 + 30); 
        }
    context.restore();
    }
    
    newWave(){
        if (Math.random()< 0.5 && this.columns * this.enemySize < this.width * 0.8 ){
        this.columns++; 
         } else if (this.rows * this.enemySize< this.height * 0.6){
        this.rows++; 
     
    }
    this.waves.push(new Wave(this));
}
    restart(){
        this.player.restart(); 
        this.columns = 2; 
        this.rows = 2; 
        this.waves = []; 
        this.waves.push(new Wave(this)); 
        this.waveCount = 1; 

        this.score = 0; 
        this.gameOver = false; 

    }
    
}


// This line makes sure we're ready to start drawing when everything on the page is ready.
window.addEventListener('load', function(){
    // This line gets a special paper from our webpage called a canvas.
    const canvas = document.getElementById('canvas1');
    
    // This line gets a set of special crayons for drawing on our canvas paper.
    // We're using the '2D' crayons because we want to draw flat pictures.
    const ctx = canvas.getContext('2d');
    
    // This line makes our canvas paper 600 pixels wide.
    canvas.width = 600;
    
    // This line makes our canvas paper 800 pixels tall.
    canvas.height = 800;

    ctx.fillStyle = 'white'; 
    ctx.strokeStyle = 'white'; 
    // ctx.lineWidth = 5;
    ctx.font= '30px Impact'; 

    const game = new Game(canvas); // Create a new game using a canvas


    let lastTime = 0; 



function animate(timeStamp){
    const deltaTime = timeStamp - lastTime;
    lastTime = timeStamp; 

    ctx.clearRect(0,0, canvas.width, canvas.height); 
    game.render(ctx, deltaTime); // Render the game
    requestAnimationFrame(animate); 



}
animate(0);
});



//{} are purple for functions, blue for conditional statements, yellow for objects and arrays, and 
