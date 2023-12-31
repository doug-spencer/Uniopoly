var socket;
var username;
const sprite_imgs = [
    'aphro_standard.webp', 'lucas_standard.webp', 'NOT CONFIRMEDmarkel_standard.webp',
     'sarah_standard.webp', 'stewart_standard.webp', 'terence_standard.webp', 'uli_standard.webp'
];
var colours = ['gold', 'blue', 'darkgreen', 'FF69B4', 'darkred', 'black'];
$(document).ready(function(){
    socket = io.connect('http://' + document.domain + ':' + location.port + '/gameroom');
    socket.on('connect', function() {
        socket.emit('join', {});
    });
    $('#buy-property-button').hide();
    $('#dont-buy-property-button').hide();
    $('#end-turn-button').hide();
    $('#dice-button').hide();

    $('#text-box').hide();
    //get username
    socket.on('get username', function(data) {
        username = data.username;
    });

    //for any basic msgs
    socket.on('message', function(data) {
        let colour = 'white';
        if (data.colourId != undefined) {
            colour = colours[data.colourId];
        }
        $('#messages').append(`<p style="margin: 0px;color: ${colour};">${data.msg}</p>`);
        // $('#messages').val($('#messages').val() + data.msg + '\n');
        $('#messages').scrollTop($('#messages')[0].scrollHeight);
    });
    // Displays text in centre of board
    socket.on('display text', function(data) {
        $('#text-box').show();
        var header = document.createElement("h1");
        header.innerHTML = data.text;
        document.getElementById("text-box").appendChild(header);
    });
    // Clears text in center of board
    socket.on('clear text', function() {
        var div = document.getElementById('text-box');
        while(div.firstChild){
            div.removeChild(div.firstChild);
        }
        $('#text-box').hide();
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

    socket.on('redirect to winner page', function(data) {
        console.log('redirect to winner page')
        window.location.href = "/winner";
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
                        <td><img src="/static/images/playerIcons/${sprite_imgs[data.players[i][0]]}" alt="image ${i}"/></td>
                        <td>${data.players[i][1]}</td>
                        <td>${data.players[i][2]}</td>
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
                socket.emit('mortgage card', {card_id: data.unmortgaged_cards_id[i], photo: data.unmortgaged_cards[i]});
            });
           document.getElementById('image-grid-unmortgaged').appendChild(img);
        }
        $("#image-grid-mortgaged").html('');
        for (let i=0; i<data.mortgaged_cards.length; i++) {
            var name = data.mortgaged_cards[i];
            const img = new Image();
            img.src = '/images/'+name;
            img.addEventListener('click', function() {
                socket.emit('unmortgage card', {card_id: data.mortgaged_cards_id[i], photo: data.mortgaged_cards[i]});
            });
            document.getElementById('image-grid-mortgaged').appendChild(img);
        }
    });
    socket.on('houses', function(data) {
        html = `<h4>You don't have any colour sets so you can't buy a house</h4>`
        if (data.houses !== undefined) {
            html = `<h4>Owned Houses:</h4>`
            html += `<table class="row-houses">`;
            for (let i=0; i<data.houses.length; i++) {
                for (let j=0; j<data.houses[i].length; j++) {
                    var name = data.houses[i][j][0];
                    html += `<tr class="house">`;
                    html += `<td><div class="${data.houses[i][j][1]} colour-square"></div></td>`;
                    html += `<td>${name}</td>`;
                    if (data.houses[i][j][2] == 0) {
                        html += `<td><button class="disabled" onclick="sell_house('${name}')" disabled>-</button>`;
                    }
                    else {
                        html += `<td><button class="minus" onclick="sell_house('${name}')">-</button>`;
                    }

                    html += `${data.houses[i][j][2]}`;

                    if (data.houses[i][j][2] == 5) {
                        html += `<button class="disabled" onclick="buy_house('${name}')" disabled>+</button></td>`;
                    }
                    else {
                        html += `<button class="plus" onclick="buy_house('${name}')">+</button></td>`;
                    }
                    html += `</tr>`;
                }
            }
            html += `</table>`;
        }
        $('#houses').html(html);
    });
    socket.on('display dice', function(data) {
        // Clears previous dice
        var div = document.getElementById('dice-display');
        while(div.firstChild){
            div.removeChild(div.firstChild);
        }

        const dice = [
            'dice_1.png', 'dice_2.png', 'dice_3.png',
            'dice_4.png','dice_5.png', 'dice_6.png',
        ];
        // Displays both dice inline
        const img1 = new Image();
        img1.src = '/static/images/dice/' + dice[data.roll1 - 1];
        img1.alt = `Die ${data.roll1}`;
        document.getElementById('dice-display').appendChild(img1);
        const img2 = new Image();
        img2.src = '/static/images/dice/' + dice[data.roll2 - 1];
        img2.alt = `Die ${data.roll2}`;
        document.getElementById('dice-display').appendChild(img2);
    });

    //players position update
    socket.on('update player positions', function(data) {
        for (let i=0; i<40; i++) {
            $('#tile' + i).html("");
        }
        $('#tile10-j').html("");
        for (let i=0; i<data.players.length; i++) {
            let players_arr = data.players[i][1].split(',');
            let symbols = data.players[i][2].split(',');
            let inJail = data.players[i][3].split(',');
            for (let j=0; j<players_arr.length; j++) {
                let id = data.players[i][0];
                if (id == 10 && inJail[j] > 0) {
                    id += '-j';
                }
                if (players_arr[j] == username) {

                    $('.tile.highlight').removeClass('highlight');
                    let row, element;
                    if (id == '10-j') {
                        row = 0;
                        element = document.getElementById(`tile${id}`).parentElement;
                    } else if (id == '10') {
                        row = 1;
                        element = document.getElementById(`tile${id}`).parentElement;
                    } else {
                        row = Math.floor(id / 10);
                        element = document.getElementById(`tile${id}`).parentElement;
                    }
                    document.getElementById('board').setAttribute('class', 'orientation' + row);
                    $('.tile.highlight').removeClass('highlight');
                    document.getElementById(`tile${id}`).parentElement.setAttribute('class', 'tile highlight');
                }
                $('#tile' + id).append('<img src="/static/images/playerIcons/' + sprite_imgs[symbols[j]] + '" alt="' + players_arr[j] + '"/>');
            }
        }
    });
    socket.on('game_over', function(data){
        window.location.href = "/menu";
    });

    socket.on('flash function', function(data) {
        const animatedText = document.getElementById('flashing-image');
        //animatedText.innerHTML = "image here";
        body = `<img src="/static/images/oakHouseKitchen.jpg" alt="Oak House Kitchen"/>`
        document.getElementById("flashing-image").innerHTML = body;
        animatedText.classList.add('flashing-image');
      
        // Remove the animation class after it finishes to allow for re-triggering
        setTimeout(() => {
            document.getElementById("flashing-image").innerHTML = "";
            animatedText.classList.remove('flashing-image');
        }, 3000); // Match the duration of the animation (3s)
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
});
function buy_property() {
    const property = document.getElementById('property').value;
    socket.emit('buy property', {property: property});
}
function bankrupt() {
    socket.emit('bankrupt');
    //var now = new Date().getTime();
    //while(new Date().getTime() < now + 1000){ /* Do nothing */ }
    //window.location.href = "/menu";
}
function close_options() {
    document.getElementById("options").style.display = 'none';
    document.getElementById("open-close").onclick = open_options;
    document.getElementById("open-close").className = 'button';
    document.getElementById("open-close").disabled = false;
    document.getElementById("open-close").innerHTML = 'View Your Cards';
}
function open_options() {
    document.getElementById("options").style.display = 'block';
    document.getElementById("open-close").onclick = 'return';
    document.getElementById("open-close").className = 'button button-disabled';
    document.getElementById("open-close").disabled = true;
    document.getElementById("cards-tab").className = 'tablinks active';
    socket.emit('get cards');
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
}, 2000); 