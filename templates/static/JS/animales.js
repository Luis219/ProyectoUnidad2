
var audio = document.querySelector('.audio');

function animaleSound(element){
    //sonidos de los animales
    var sound = element.getAttribute('data-sound');
    audio.src= sound;
    audio.play();
}

var contador;
function calificar(item) {
    console.log(item);
    contador = item.id[0];
    let nombre = item.id.substring(1);

    for (let i = 0; i < 5; i++) {
        //i=0
        //i=1
        //i=2
        //i=3
        //i=4
        //if(4<2)
        if (i < contador) {
            //primera vez 0+1 = 1estrella;
            //primera vez 1+1 = 2estrella;
            //primera vez 2+1 = 3estrella;
            //primera vez 3+1 = 4estrella;
            document.getElementById((i + 1) + nombre).style.color = "orange"

        } else {
            document.getElementById((i + 1) + nombre).style.color = "black"
        }
    }
    alert(contador)


}
function enviarValoracion(){
    alert(contador);
    $.ajax({
        url:"{{url_for('obtenerDatos')}}",
        type:"POST",
        data: {num:contador},
        dataType:"json",
        success:function(response){
            console.log(response)
        },
        error: function(err){
            console.log(err);
        }
       
    
    });

}

   
