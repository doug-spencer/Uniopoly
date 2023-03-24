var socket;
$(document).ready(function() {
    socket = io.connect('http://' + document.domain + ':' + location.port + '/menu');
});

function flash() {
    const animatedText = document.getElementsByClass('flash message');
    animatedText.classList.add('flashing-text');
  
    // Remove the animation class after it finishes to allow for re-triggering
    setTimeout(() => {
      animatedText.innerHTML = " ";
      animatedText.classList.remove('flashing-text');
    }, 3000); // Match the duration of the animation (3s)
  }
