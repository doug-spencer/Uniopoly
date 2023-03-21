//runs on refresh or load of lobby
var username;
$(document).ready(function() {
    socket = io.connect('http://' + document.domain + ':' + location.port + '/lobby');
    
    socket.on('connect', function(){
      socket.emit('join', {});
    });

    socket.on('flash function', function(data) {
      const animatedText = document.getElementById('flashing-text');
      animatedText.innerHTML = data.msg + " entered the room";
      animatedText.classList.add('flashing-text');
    
      // Remove the animation class after it finishes to allow for re-triggering
      setTimeout(() => {
        animatedText.innerHTML = "";
        animatedText.classList.remove('flashing-text');
      }, 3000); // Match the duration of the animation (3s)
    })

    socket.on('game started', function(data) {
        window.location.href = "http://" + document.domain + ":" + location.port + "/gameroom"
    });
    
    //get username
    socket.on('get username', function(data) {
      username = data.username;
    });
    //gathers the player list
    //adds the players to a table with a remove button 
    socket.on('player list', function(data) {
      var isNotHost = data.username != data.players[0];
      var body = '';
      for(var i=0; i<data.players.length; i++){
        if (isNotHost || i == 0) {
          body += `<tr class="table-rows"><td>Player ${i+1}</td><td>${data.players[i]}</td><td></td></tr>`
        } else {
          body += `<tr class="table-rows"><td>Player ${i+1}</td><td>${data.players[i]}</td><td><button class="button" type="button" onclick="remove_player('${data.players[i]}')">Remove</button></td></tr>`
        }
      }
      document.getElementById("table-body").innerHTML = body;
      if (isNotHost) {
        document.getElementById("start").style.display = "none";
      }
    });
    
    socket.emit('check pregame status');
    socket.on('player not in game', function() {
      window.location.href = "http://" + document.domain + ":" + location.port + "/menu"
    });
});

function remove_player(name_of_player_to_remove){
  socket.emit('remove', {username:name_of_player_to_remove})
}

//calls function every 2.5seconds
setInterval(function() {
    socket.emit('check pregame status');
}, 2500); 