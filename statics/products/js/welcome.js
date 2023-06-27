document.addEventListener('DOMContentLoaded', function() {
    var banner = document.getElementById('banner');
    var closeBtn = document.getElementById('close-btn');
    

    // Cerrar el banner después de 5 segundos
    // setTimeout(function() {
    // closeBanner();
    // }, 15000);

    // Cerrar el banner al hacer clic en el botón de cierre
    closeBtn.addEventListener('click', function() {
    closeBanner();
    });

      // Cerrar el banner cuando el video termine de reproducirse
  video.addEventListener('ended', function() {
    closeBanner();
  });

    // Función para cerrar el banner
    function closeBanner() {
    banner.style.display = 'none';
    }

    
});


// cotizador desplazarse
function scrollToSection(sectionId) {
  const section = document.querySelector(sectionId);
  section.scrollIntoView({ behavior: 'smooth' });
}


// botones

// Obtener el elemento que contiene los botones
var botonesDinamicos = document.querySelector('.botones-dinamicos');

// Obtener el punto de inicio para mostrar u ocultar los botones
var puntoInicio = 480; // Puedes ajustar este valor según tus necesidades

// Función para comprobar la posición del scroll y mostrar u ocultar los botones
function mostrarUOcultarBotones() {
  // Obtener la posición actual del scroll
  var scrollPos = window.pageYOffset || document.documentElement.scrollTop;

  // Comparar la posición del scroll con el punto de inicio
  if (scrollPos >= puntoInicio) {
    botonesDinamicos.style.display = 'block'; // Mostrar los botones
  } else {
    botonesDinamicos.style.display = 'none'; // Ocultar los botones
  }
}

// Escuchar el evento scroll y llamar a la función mostrarUOcultarBotones
window.addEventListener('scroll', mostrarUOcultarBotones);
