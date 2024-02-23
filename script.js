class Player {
    constructor(game){
        this.game= game; 
        this.width= 100;
        this.height= 100;
        
        this.x = this.game.width * 0.5; 
        this.y = this.game.height- this.height; 
        this.speed = 5; 
    }
    draw(context){
        context.fillRect(this.x, this.y, this.width, this.height); 
      
    }
    update(){
        // horizontal movement 
        if (this.game.keys.indexOf('ArrowLeft') > -1) this.x -= this.speed;
        if (this.game.keys.indexOf('ArrowRight') > -1) this.x += this.speed;

        //horizontal boundaries prevents from going outside of the box
        if (this.x < -this.width * 0.5) this.x = -this.width * 0.5;
        else if (this.x > this.game.width - this.width * 0.5) this.x = this.game.width -this.width *0.5;

    }
    shoot(){
        const projectile = this.game.getProjectile()
        if (projectile) projectile.start(this.x + this.width * 0.5, this.y); 


    }
}

class Projectile {
    constructor(){
        this.width = 4; 
        this.height = 20; 
        this.x = 0;  
        this.y = 0; 
        this.speed = 20 
        this.free = true; //object pool cleaning and garbage collection

    }
    draw(context){
        if (!this.free){
            context.fillRect(this.x,this.y, this.width, this.height);    
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

    }
    draw(context){
        context.strokeRect(this.x, this.y, this.width, this.height); 
    }
    update(x,y){
        this.x = x + this.positionX; 
        this.y = x + this.positionY; 
    }
}

class Wave {
    constructor(game){
        this.game = game; 
        this.width = this.game.columns * this.game.enemySize; 
        this.height= this.game.rows * this.game.enemySize; 
        this.x = 0; 
        this.y = 0;
        this.speedX = 3; 
        this.speedY = 0; 
        this.enemies = []; 
     }
     render(context) {
        this.speedY = 0;
        context.strokeRect(this.x, this.y, this.width, this.height); // Draw outline
        this.x += this.speedX;
        if (this.x < 0 || this.x > this.game.width - this.width){
            this.speedX *= -1; 
            this.speedY = this.game.enemySize;
        }
            this.x += this.speedX;
            this.y += this.speedY;
     }
     create(){
            for (let y = 0; y < this.game.rows; y++){
                for (let x = 0; x < this.game.columns; x++) {
                    let enemyX = x * this.game.enemySize; 
                    let enemyY = y * this.game.enemySize; 

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
        this.numberOfProjectiles = 10; 
        this.createProjectiles(); 

        this.columns = 3; 
        this.rows = 3; 
        this.enemySize = 60;

        this.waves = []; 

        this.waves.push(new Wave(this)); 

        //event listeners for key board functions
        window.addEventListener('keydown', e => {
            if (this.keys.indexOf(e.key) === -1) this.keys.push(e.key)//push method add the specified elements to the end of an array and regurns the new length of the array.
            if (e.key === '1') this.player.shoot(); 
           
        })
        window.addEventListener('keyup', e => {
            const index = this.keys.indexOf(e.key);
            if (index > -1) {
                this.keys.splice(index, 1);
               
            }
        });
        
    }
    render(context){
       
        this.player.draw(context); 
        this.player.update(); 
        this.projectilesPool.forEach(projectile => {
            projectile.update(); 
            projectile.draw(context); 
        })
        this.waves.forEach(wave => {
            wave.render(context);

        })
    }

    createProjectiles(){
            for (let i = 0; i < this.numberOfProjectiles; i++){
                this.projectilesPool.push(new Projectile()); // this is like putting the new bullet we made into our box of bullers

            }
    }
    getProjectile () {
            for (let i = 0; i < this.projectilesPool.length; i++){
                if (this.projectilesPool[i].free) return this.projectilesPool[i]; 
            }

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
    ctx.lineWidth = 5;

    const game = new Game(canvas); // Create a new game using a canvas
    // game.createProjectiles(); //CHATGPT!!!!!!!!!!!!!!!!!!!!



function animate(){
    ctx.clearRect(0,0, canvas.width, canvas.height); 
    game.render(ctx); // Render the game
    requestAnimationFrame(animate); 



}
animate();
});



//{} are purple for functions, blue for conditional statements, yellow for objects and arrays, and 
