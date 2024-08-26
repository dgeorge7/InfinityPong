import { Scene } from 'phaser';

export class MainMenu extends Scene
{
    constructor ()
    {
        super('MainMenu');
    }

    create ()
    {
        this.add.image(960, 540, 'background');

        this.add.image(940, 520, 'logo');

        const theme = this.sound.add('theme');

        theme.play();

        theme.setLoop(true);

        this.add.text(960, 620, 'Play', {
            fontFamily: 'Arial Black', fontSize: 38, color: '#ffffff',
            stroke: '#000000', strokeThickness: 8,
            align: 'center'
        }).setOrigin(0.5);

        this.input.once('pointerdown', () => {

            theme.stop(); 
            this.scene.start('Game');

        });
    }
}
