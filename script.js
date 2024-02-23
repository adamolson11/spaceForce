class Player {
    constructor(game){
        this.game= game; 
        this.width= 100;
        this.height= 100;
        
        this.x = this.game.width * 0.5; 
        this.y = this.game.height- this.height; 
        this.speed = 0; 
    }
    draw(context){
        context.fillRect(this.x, this.y, this.width, this.height); 
      
    }
    update(){
        this.x += this.speed= 0;
    }
}

class Projectile {

}

class Enemy {

}

class Game {
    constructor(canvas){//blueprint for canvas 
        this.canvas = canvas; //local instance of canvas limits it within the object
        this.width = this.canvas.width; //local instance of width and height
        this.height = this.canvas.height;
        this.keys = []; 
        this.player = new Player(this)

        //event listeners for key board functions
        window.addEventListener('keydown', e => {
            if (this.keys.indexOf(e.key) === -1) this.keys.push(e.key)//push method add the specified elements to the end of an array and regurns the new length of the array.
            console.log(this.keys); 
        })
        window.addEventListener('keyup', e => {
            const index = this.keys.indexOf(e.key);
            if (index > -1) {
                this.keys.splice(index, 1);
                console.log(this.keys);
            }
        });
        
    }
    render(context){
        // console.log(this.width, this.height); 
        this.player.draw(context); 
        this.player.update(); 
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

    const game = new Game(canvas); // Create a new game using a canvas
// console.log(game); // Display the game object in the console

function animate(){
    ctx.clearRect(0,0, canvas.width, canvas.height); 
    game.render(ctx); // Render the game
    requestAnimationFrame(animate); 



}
animate();
});

