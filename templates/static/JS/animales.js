
var audio = document.querySelector('.audio');

function animaleSound(element){
    var sound = element.getAttribute('data-sound');
    audio.src= sound;
    audio.play();
}

