//runs on refresh or load of lobby
var username;
$(document).ready(function() {
    socket = io.connect('http://' + document.domain + ':' + location.port + '/lobby');
    
    socket.on('connect', function(){
      socket.emit('join', {});
    });

    socket.on('flash function', function(data) {
      console.log('bosh')
      const animatedText = document.getElementById('flashing-text');
      animatedText.innerHTML = data.msg + " entered the room";
      animatedText.classList.add('flashing-text');
    
      // Remove the animation class after it finishes to allow for re-triggering
      setTimeout(() => {
        animatedText.innerHTML = " ";
        animatedText.classList.remove('flashing-text');
      }, 3000); // Match the duration of the animation (3s)
    })

    socket.on('start game avalible', function() {
      console.log('boshhhh')
      var input = document.getElementById('start')
      input.disabled = false
      input.className = 'button'
    })

    socket.on('start game not avalible', function() {
      console.log('not boshhhh')
      var input = document.getElementById('start')
      input.disabled = true
      input.className = 'button disabled'
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
      var body = `<tr class="table-rows host"><td class="col"><p>${data.players[0]}</p><button class="button" type="button" onclick="remove_player('${data.players[i]}')">Remove</button></td></tr>`;
      for(var i=1; i<data.players.length; i++){
        if (isNotHost) {
          body += `<tr class="table-rows hidden-button"><td class="col"><p>${data.players[i]}</p><button class="button" type="button" onclick="remove_player('${data.players[i]}')">Remove</button></td></tr>`;
        } else {
          body += `<tr class="table-rows"><td class="col"><p>${data.players[i]}</p><button class="button remove" type="button" onclick="remove_player('${data.players[i]}')">Remove</button></td></tr>`;
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