import { Scene } from 'phaser';

export class Preloader extends Scene
{
    constructor ()
    {
        super('Preloader');
    }

    init ()
    {
        
        //  A simple progress bar. This is the outline of the bar.
        this.add.rectangle(960, 540, 468, 32).setStrokeStyle(1, 0xffffff);

        //  This is the progress bar itself. It will increase in size from the left based on the % of progress.
        const bar = this.add.rectangle(960-230, 540, 4, 28, 0xffffff);

        //  Use the 'progress' event emitted by the LoaderPlugin to update the loading bar
        this.load.on('progress', (progress) => {

            //  Update the progress bar (our bar is 464px wide, so 100% = 464px)
            bar.width = 4 + (460 * progress);

        });
    }

    preload ()
    {
        //  Load the assets for the game - Replace with your own assets
        this.load.setPath('assets');

        this.load.image('background', 'images/bg.jpg');

        this.load.image('stage', 'images/bg1.jpg');

        this.load.image('logo', 'images/glogo.png');

        this.load.spritesheet('ball', 'images/ball.png', { frameWidth: 25, frameHeight: 25 });

        this.load.spritesheet('player', 'images/player.png', { frameWidth: 89, frameHeight: 152 });

        this.load.spritesheet('opponent', 'images/cpu.png', { frameWidth: 89, frameHeight: 152 });

        this.load.audio('theme', [ 'music/Infinity Pong Theme.mp3' ]);

        this.load.audio('gtheme', [ 'music/Infinity Pong France Theme.mp3' ]);

        this.load.audio('hit', [ 'music/ping.wav' ]);

    }

    create ()
    {
   

        this.add.text(960, 620, 'Ready to be a winner?', {
            fontFamily: 'Arial Black', fontSize: 38, color: '#ffffff',
            stroke: '#000000', strokeThickness: 8,
            align: 'center'
        }).setOrigin(0.5);

        

        this.input.once('pointerdown', () => {
            

            this.scene.start('MainMenu');

        });
    }

}
