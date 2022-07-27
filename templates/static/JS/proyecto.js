var baseHeight = 720;
var screenRatio = window.innerWidth / window.innerHeight;
var gameWidth = baseHeight / screenRatio;
var game = new Phaser.Game(baseHeight, gameWidth, Phaser.AUTO);

var App = {};

App.Intro = {
    preload: function() {
        game.load.audio("yes", ["../static/sonidos/yes.mp3", "../static/sonidos/yes.ogg"]);
        game.load.audio("no", ["../static/sonidos/no.mp3", "../static/sonidos/no.ogg"]);
        game.load.image("logo", "../static/imagenes/zk.png");
        game.load.image("bg", "../static/imagenes/bg.jpg");
        game.load.image("playbtn1", "../static/imagenes/playsound1.png");
        game.load.image("playbtn2", "../static/imagenes/playsoundpressed.png");
    },
    create: function() {
        game.stage.backgroundColor = "#ffffff";
        game.scale.scaleMode = Phaser.ScaleManager.EXACT_FIT;
        var zkLogo = game.add.sprite(game.world.centerX, game.world.centerY, "logo");
        zkLogo.anchor.setTo(.5);
        zkLogo.scale.setTo(1);
        game.camera.flash(0x000000, 1000);
        setTimeout(function() {
            game.state.start("main");
        }, 4000);
    }
}

var isPaused = false;
var currentSound;
var snd;
var sndCorrect;
var sndWrong;
App.Main = {
    //Funcion de precarga de datos
    preload: function() {
        for(var i = 0; i < 10; i++){
            game.load.image("animage" + (i+1), "../static/imagenes/anm" + (i+1) + ".png");
        }
        game.load.image("unknown", "../static/imagenes/unknown.png");
        currentSound = game.rnd.integerInRange(1, 10);
        game.load.audio("currentSound", ["../static/sonidos/sound" + currentSound + ".mp3", "../static/sonidos/sound" + currentSound + ".ogg"]);
        game.load.audio("yes", ["../static/sonidos/yes.mp3", "../static/sonidos/yes.ogg"]);
        game.load.audio("no", ["../static/sonidos/no.mp3", "../static/sonidos/no.ogg"]);
    },
    create: function() {
        /**Función que reproduce el audio actual */
        isPaused = false;
        snd = game.add.audio("currentSound", 1, false);
        snd.onStop.add(soundStopped, this);
        sndCorrect = game.add.audio("yes", 1, false);
        sndWrong = game.add.audio("no", 1, false);
        var bg = game.add.sprite(0, 0, "bg");
        bg.width = game.width;
        bg.height = game.height;
        
        this.playbtn = game.add.sprite(game.width/2, game.height/4, "playbtn1");
        this.playbtn.anchor.setTo(.5);
        this.playbtn.scale.setTo(1.5);
        this.playbtn.inputEnabled = true;
        this.playbtn.events.onInputDown.add(playCurrentSound, this);
        fadeInTween(this.playbtn, 0);
        
        this.unknown = game.add.sprite(game.width/2 + 150, game.height/2, "unknown");
        this.unknown.anchor.setTo(.5);
        fadeInTween(this.unknown, 500);
        this.unknown = game.add.sprite(game.width/2 - 150, game.height/2, "unknown");
        this.unknown.anchor.setTo(.5);
        fadeInTween(this.unknown, 250);
        
        showGt("Tap speaker button to listen animal sound.");
        

        function soundStopped(){
            /**Función que detiene el sonido y en la que se determina la respuesta correcta */
            console.log("Sonido detenido / Sound stopped");
            showGt("What animal was that?/ ¿Qué animal es ?")
            isPaused = false;
            
            //determine, left or right to be correct answer
            if(game.rnd.integerInRange(0, 1) == 0){
                //correct answer is left one
                this.test1 = game.add.sprite(game.width/2 + 150, game.height/2, "animage" + getRandomImage());
                this.test1.anchor.setTo(.5);
                this.test1.inputEnabled = true;
                this.test1.events.onInputDown.add(function(){
                    checkAnswer(0, this.test1);
                }, this);
                this.test2 = game.add.sprite(game.width/2 - 150, game.height/2, "animage" + currentSound);
                this.test2.anchor.setTo(.5);
                this.test2.inputEnabled = true;
                this.test2.events.onInputDown.add(function(){
                    checkAnswer(1, this.test2);
                }, this);
            }else{
                //right one
                this.test1 = game.add.sprite(game.width/2 + 150, game.height/2, "animage" + currentSound);
                this.test1.anchor.setTo(.5);
                this.test1.inputEnabled = true;
                this.test1.events.onInputDown.add(function(){
                    checkAnswer(1, this.test1);
                }, this);
                this.test2 = game.add.sprite(game.width/2 - 150, game.height/2, "animage" + getRandomImage());
                this.test2.anchor.setTo(.5);
                this.test2.inputEnabled = true;
                this.test2.events.onInputDown.add(function(){
                    checkAnswer(0, this.test2);
                }, this);
            }
        }
    }
}

game.state.add("intro", App.Intro);
game.state.add("main", App.Main);
game.state.start("intro");

function playCurrentSound(element){
    //Reproudcción de osnido actual
    if(!isPaused){
        isPaused = true;
        console.log("clicked");
        snd.play();
        fadeInTween(element, 0);
        showGt("Listen...")
    }
}

function getRandomImage(){
    //Obtener imágenes de forma random
    var rimg = currentSound;
    while(rimg == currentSound){
        rimg = game.rnd.integerInRange(1, 10);
    }
    return rimg;
}

function checkAnswer(x, element){
    //Verificar la respuesta correcta

    score=0;
    if(!isPaused){
        isPaused = true;
        
        if(x == 0){
            console.log("Incorrecto!");
            showGt("<h1>Incorrecto!</h1>");
            sndWrong.play();
        }else{
           
            showGt("<h1>Correcto!</h1>");
           // score=score;
       
            console.log("Correcto!");
            
            sndCorrect.play();
            score=score+1;
             
            
            
          
                
        
            
            /** 
            showGt("<h2></h2>",score);
            */
        }
        verScore(score)
        setTimeout(function(){
            game.state.start("main");
        }, 2000);
        btnTween(element, 0);
    }
}

function verScore(score){
    score+=1;
    

   
    console.log(score);
}

function fadeInTween(element, delay){
    element.alpha = 0;
    game.add.tween(element).to( { alpha : 1 }, 300, Phaser.Easing.Linear.None, true, delay);
}

function btnTween(element, delay){
    element.scale.setTo(1.1);
    game.add.tween(element.scale).to( { x : 1, y : 1 }, 1000, Phaser.Easing.Linear.None, true, delay);
}

function showGt(text){
    $("#juegotexto").hide().html(text).fadeIn();
}