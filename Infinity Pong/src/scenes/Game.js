import { Scene } from 'phaser';

export class Game extends Scene
{

    constructor ()
    {
        super('Game');
    }

    create ()
    {
        this.physics.world.setBoundsCollision(true, true, false, false);


        this.gtheme = this.sound.add('gtheme');

        this.gtheme.play();

        this.gtheme.setLoop(true);

        this.add.image(960, 540, 'stage');



        this.net = this.add.rectangle(960, 540, 468, 15, 0xffffff);

        this.physics.add.existing(this.net, false);

        this.net.body.setBounce(1, 1);

        this.net.body.setAllowGravity(false);

        this.net.body.setAllowDrag(false);

        this.net.body.onWorldBounds = true;

        this.net.body.setCollideWorldBounds(true);

        this.net.body.pushable = false;

        this.net.body.setVelocity(800, 0);



        this.ball = this.physics.add.sprite(960, 700, 'ball');

        this.ball.setCircle(12.5);

        this.ball.body.setBounce(1, 1);
        
        this.ball.body.setCollideWorldBounds(true);

        this.ball.body.setAllowGravity(false);

        this.ball.body.setAllowDrag(false);

        this.ball.body.onWorldBounds = true;


        if(this.input.activePointer.y < this.net.getBottomCenter().y + 80) 
            this.player = this.physics.add.sprite(this.input.activePointer.x, this.net.getBottomCenter().y + 80, 'player');
        else
            this.player = this.physics.add.sprite(this.input.activePointer.x, this.input.activePointer.y, 'player');

        this.player.body.setAllowGravity(false);

        this.player.body.setAllowDrag(false);

        this.player.body.setCollideWorldBounds(true);

        this.player.body.onWorldBounds = true;

        this.player.body.setDirectControl();
        
        this.player.body.pushable = false;

        this.player.setImmovable(true);



        this.opponent = this.physics.add.sprite(this.ball.x, this.net.getTopCenter().y - 220, 'opponent');

        this.opponent.flipY = true;

        this.opponent.body.setAllowGravity(false);

        this.opponent.body.setAllowDrag(false);

        this.opponent.body.setCollideWorldBounds(true);

        this.opponent.body.onWorldBounds = true;
        
        this.opponent.body.pushable = false;

        this.opponent.setImmovable(true);

        




        this.input.activePointer.smoothFactor = 0.5;



        const hit = this.sound.add('hit');
       


        this.physics.add.collider(this.player, this.ball, 
            

            function(player, ball){  
                
                hit.play();
                if(ball.body.x  > player.body.x - 40 && ball.body.x < player.body.x)
                    ball.body.setVelocity(-1300, -950);
                else if(ball.body.x  < player.body.x + 40 && ball.body.x > player.body.x)
                    ball.body.setVelocity(1300, -950);
                else if(ball.body.x  < player.body.x - 40)
                    ball.body.setVelocity(-1500, -750);
                else if(ball.body.x  > player.body.x + 40)
                    ball.body.setVelocity(1500, -750);
           
            
            }
        );


        this.physics.add.collider(this.opponent, this.ball, 
            

            function(op, ball){  
                
                hit.play();
                if(ball.body.x  > op.body.x - 40 && ball.body.x < op.body.x)
                    ball.body.setVelocity(1300, 950);
                else if(ball.body.x  < op.body.x + 40 && ball.body.x > op.body.x)
                    ball.body.setVelocity(-1300, 950);
                else if(ball.body.x  < op.body.x - 40)
                    ball.body.setVelocity(1500, 750);
                else if(ball.body.x  > op.body.x + 40)
                    ball.body.setVelocity(-1500, 750);
           
            
            }
        );


        this.physics.add.collider(this.ball, this.net, 
            

            function(ball, net){  
                
                hit.play();
            
            }
        );



        this.physics.world.on('worldbounds', 

            function(ball, up, down, left, right){  
                    
                if(ball.pushable && (left || right))
                    hit.play();
            
            }
        
        );


        this.input.keyboard.once('keydown-SPACE', () => {

            this.scene.start('GameOver');
            this.gtheme.stop();

        });

    }


    update() {

  
        this.physics.world.wrap(this.ball);
        this.physics.world.wrap(this.net);
     //   if(this.ball.y > this.opponent.y)
      //      this.opponent.x = this.ball.x;
        this.player.x = this.input.activePointer.x;
        this.opponent.x = this.input.activePointer.x;


        if(this.input.activePointer.y >= this.net.getBottomCenter().y + 80) {
            this.player.y = this.input.activePointer.y;
        }
        else {
            this.player.y = this.net.getBottomCenter().y + 80;

        }



        const angIncrement = 160/1920;
        if(this.player.x < 960)
            this.player.setAngle(0 - (angIncrement * (960 - this.player.x)));
        else if(this.player.x > 960)
            this.player.setAngle((angIncrement * (this.player.x - 960)));
        else if(this.player.x == 960)
            this.player.setAngle(0);


        if(this.opponent.x < 960)
            this.opponent.setAngle((angIncrement * (960 - this.opponent.x)));
        else if(this.opponent.x > 960)
            this.opponent.setAngle((-angIncrement * (this.opponent.x - 960)));
        else if(this.opponent.x == 960)
            this.opponent.setAngle(0);


    /*    if(this.ball.y <= this.net.getTopCenter().y - 80 && this.ball.y >= this.opponent.y) {

            this.physics.moveTo(this.opponent, this.ball.x, this.ball.y - 43, 500);
            //this.opponent.y = this.ball.y - 43;
        }
        else
            this.physics.moveTo(this.opponent, this.ball.x, this.net.getTopCenter().y - 270, 500);
       */

        

    }



}
