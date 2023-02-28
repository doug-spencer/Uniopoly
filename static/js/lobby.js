//runs on refresh or load of lobby
$(document).ready(function() {
    socket = io.connect('http://' + document.domain + ':' + location.port + '/lobby');
    socket.on('game started', function(data) {
        window.location.href = "http://" + document.domain + ":" + location.port + "/gameroom"
    });
    //gathers the player list
    //adds the players to a table with a remove button 
    socket.on('player list', function(data) {
    table = document.getElementById("playersTable");

      table.innerHTML = `<tr><td>Player 1</td><td>${data.players[0]}</td></tr>`;
      for(var i=1; i<data.players.length; i++){
        var row = `<tr>
                      <td>Player ${i+1}</td>
                      <td>${data.players[i]}</td>
                      <td><button type="button" onclick="remove_player('${data.players[i]}')">Remove</button></td>
                    </tr>`
        table.innerHTML += row
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