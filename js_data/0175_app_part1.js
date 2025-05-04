let pronombre = ['los', 'esos', 'nuestros'];
let adjetivo = ['bonitos', 'dulces', 'originales' ];
let sustantivo = ['cohetes', 'videojuegos', 'juegos', 'abrigos', 'guantes'];
let pagina = ['.com', '.es', '.mx', '.store'];
  
  for(let i = 0; i < pronombre.length; i++) {
    for(let j = 0; j < adjetivo.length; j++) {
      for (let k = 0; k < sustantivo.length; k++) {
        for (let l = 0; l < pagina.length; l++) {
            console.log(pronombre[i] + adjetivo[j] + sustantivo[k] + pagina[l]); 
        }
      }
    }
  }