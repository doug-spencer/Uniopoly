var socket;
var username;
$(document).ready(function(){
    socket = io.connect('http://' + document.domain + ':' + location.port + '/gameroom');
    socket.on('connect', function() {
        socket.emit('join', {});
    });
    $('#buy-property-button').hide();
    $('#dont-buy-property-button').hide();
    $('#end-turn-button').hide();
    $('#dice-button').hide();

    $('#card-box').hide();
    //get username
    socket.on('get username', function(data) {
        username = data.username;
    });

    //for joining and leaving room
    socket.on('status', function(data) {
        $('#messages').val($('#messages').val() + data.msg + '\n');
        $('#messages').scrollTop($('#messages')[0].scrollHeight);
    });

    //for any basic msgs
    socket.on('message', function(data) {
        $('#messages').val($('#messages').val() + data.msg + '\n');
        $('#messages').scrollTop($('#messages')[0].scrollHeight);
    });
    socket.on('display card', function(data) {
        $('#card-box').show();
        document.getElementById("card-text").innerHTML = data.text;
    });

    //show or hide roll dice button
    socket.on('roll dice button change', function(data) {
        if(data.operation == 'show'){
            $('#dice-button').show();
        } else {
            $('#dice-button').hide();
        };
    });

    //show or hide end turn button
    socket.on('end turn button change', function(data) {
        if(data.operation == 'show'){
            console.log('fucj yu ')
            $('#end-turn-button').show();
        } else {
            $('#end-turn-button').hide();
        };
    });

    //show or hide buy property button  
    socket.on('buy property button change', function(data) {
        if(data.operation == 'show'){
            $('#buy-property-button').show();
            $('#dont-buy-property-button').show();
        } else {
            $('#buy-property-button').hide();
            $('#dont-buy-property-button').hide();
        };
        
    });
    //show roll value of dice roll
    socket.on('dice_roll', function(data) {
        document.getElementById('dice').innerHTML = 'dice value: ' + data.dice_value + ' new position: ' + data.position
        //$('dice').val('dice value: ' + data.dice_value + ' new position: ' + data.position);
    });
    //update the leaderboard
    socket.on('update leaderboard', function(data) {
        for (let i=0; i<data.players.length-1; i++) {
            for (let j=0; j<data.players.length-1-i; j++) {
                if (data.players[j][1] < data.players[j+1][1]) {
                    let temp = data.players[j];
                    data.players[j] = data.players[j+1];
                    data.players[j+1] = temp;
                }
            }
        }
        let body = "";
        for (let i=0; i<data.players.length; i++) {
            body += `<tr class="table-rows">
                        <td>${data.players[i][0]}</td>
                        <td>${data.players[i][1]}</td>
                    </tr>`;
        }
        $('#table-body').html(body);
    });
    socket.on('cards', function(data) {
        $("#image-grid-unmortgaged").html('');
        for (let i=0; i<data.unmortgaged_cards.length; i++) {
            var name = data.unmortgaged_cards[i];
            const img = new Image();
            img.src = '/images/'+name;
            img.addEventListener('click', function() {
                socket.emit('mortgage card', {card_id: data.unmortgaged_cards_id[i]});
            });
           document.getElementById('image-grid-unmortgaged').appendChild(img);
        }
        $("#image-grid-mortgaged").html('');
        for (let i=0; i<data.mortgaged_cards.length; i++) {
            var name = data.mortgaged_cards[i];
            const img = new Image();
            img.src = '/images/'+name;
            img.addEventListener('click', function() {
                socket.emit('unmortgage card', {card_id: data.mortgaged_cards_id[i]});
            });
            document.getElementById('image-grid-mortgaged').appendChild(img);
        }
    });
    socket.on('houses', function(data) {
    console.log(data.houses);
    if (data.houses !== undefined) {
        html = "";
        console.log("in loop on houses");
        for (let i=0; i<data.houses.length; i++) {
            html += `<div class="row-houses">`
            for (let j=0; j<data.houses[i].length; j++) {
                var name = data.houses[i][j][0];
                console.log(data.houses);
                console.log(name+data.houses[i][j][2]);
                html += `<div class="house">`
                html += `<button onclick="sell_house('${name}')">-</button>`;
                html += `<p>${name}</p>`;
                html += `<p>${data.houses[i][j][2]}</p>`;
                html += `<button onclick="buy_house('${name}')">+</button>`;
                html += `</div>`;
            }
            html += `</div>`;
        console.log(html)
        }
    }
    else  {
        html = `<p>"You don't have any colour sets so you can't buy a house"</p>`
    }
    $('#houses').html(html);
    });
    //players position update
    socket.on('update player positions', function(data) {
        console.log("positions updated, username: " + username);
        for (let i=0; i<40; i++) {
            $('#tile' + i).html("");
        }
        for (let i=0; i<data.positions.length; i++) {
            if (data.positions[i][1] == username) {
                let row = $('#tile' + data.positions[i][0]).parent().parent().attr('id').slice(-1);
                document.getElementById('board').setAttribute('class', 'orientation' + row);
                // $('#board').className = 'orientation' + row;
            }
            $('#tile' + data.positions[i][0]).append("<b>" + data.positions[i][1] + "</b>");
        }
    });
    //when the send message box is pressed
    $('form').submit(function(e) {
        e.preventDefault();
        text = $('#text').val();
        $('#text').val('');
        socket.emit('text', {msg: text});
    });
    //when the roll dice box is pressed
    $('#roll-dice').click(function(data) {
        $('#dice-button').hide();
        socket.emit('roll dice');
    });
    //when the end turn button is pressed
    $('#end-turn').click(function(data) {
        $('#end-turn-button').hide();
        socket.emit('end turn');
    });
    //when the buy button is pressed
    $('#buy-property').click(function(e) {
        $('#buy-property-button').hide();
        $('#dont-buy-property-button').hide();
        socket.emit('buy-property');
    });
    //when the dont buy button is pressed
    $('#dont-buy-property').click(function(e) {
        $('#buy-property-button').hide();
        $('#dont-buy-property-button').hide();
        socket.emit('dont-buy-property');
    });
    //when the card display button is pressed
    $('#card-button').click(function(e) {
        $('#card-box').hide();
    });
});
//if a player leaves the room (WIP)
function leave_room() {
    socket.emit('left', {}, function() {
        socket.disconnect();
        window.location.href = "/menu";
    });
}
function buy_property() {
    const property = document.getElementById('property').value;
    socket.emit('buy property', {property: property});
}
function close_options() {
    document.getElementById("options").style.display = "none";
  }
function open_options() {
    document.getElementById("options").style.display = "block";
}
function sell_house(name){
    console.log("selling house");
    socket.emit('sell house', {house: name});
    var now = new Date().getTime();
    while(new Date().getTime() < now + 1000){ /* Do nothing */ }
    socket.emit('get houses')
}
function buy_house(name){
    console.log("buying house");
    socket.emit('buy house', {house: name});
    var now = new Date().getTime();
    while(new Date().getTime() < now + 1000){ /* Do nothing */ }
    socket.emit('get houses')
}
function change_tab(evt, tab_name) {
    // Declare all variables
    var i, tabcontent, tablinks;
  
    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
  
    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
  
    // Show the current tab, and add an "active" class to the link that opened the tab
    document.getElementById(tab_name).style.display = "block";
    evt.currentTarget.className += " active";

    if(tab_name == "cards"){
        console.log("clicked on card")
        socket.emit('get cards');
    }
    if(tab_name == "houses"){
        console.log("didn click on card")
        socket.emit('get houses');
    }
  }
//calls function every 2.5seconds
setInterval(function() {
    socket.emit('update turn');
}, 2500); 