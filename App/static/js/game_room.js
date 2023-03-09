var socket;
$(document).ready(function(){
    socket = io.connect('http://' + document.domain + ':' + location.port + '/gameroom');
    socket.on('connect', function() {
        socket.emit('join', {});
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
    //show or hide roll dice button
    socket.on('roll dice button change', function(data) {
        if(data.operation == 'show'){
            $('#dice-button').show();
        } else {
            $('#dice-button').hide();
        };
    });
        //show or hide buy property button
        socket.on('buy property button change', function(data) {
            if(data.operation == 'show'){
                $('#buy-property-button').show();
            } else {
                $('#buy-property-button').hide();
            };
        });
    //show roll value of dice roll
    socket.on('dice_roll', function(data) {
        document.getElementById('dice').innerHTML = 'dice value: ' + data.dice_value + ' new position: ' + data.position
        //$('dice').val('dice value: ' + data.dice_value + ' new position: ' + data.position);
    });
    //players position update
    socket.on('player positions', function(data) {
        document.getElementById('test-box').innerHTML = 'players position: ' + data.positions;
        for (i = 0; i < data.postions.length; i++) {
            var position = toString(data.postions[i][0]);
            document.getElementById('tile' + position).innerHTML = data.postions[i][1];
        }
    });
    //when the send message box is pressed
    $('#send').click(function(e) {
        text = $('#text').val();
        $('#text').val('');
        socket.emit('text', {msg: text});
    });
    //when the roll dice box is pressed
    $('#roll-dice').click(function(e) {
        $('#dice-button').hide();
        socket.emit('roll dice');
    });
    //when the roll dice box is pressed
    $('#buy-property').click(function(e) {
        $('#buy-property').hide();
        socket.emit('buy-property');
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
  }
//calls function every 2.5seconds
setInterval(function() {
    socket.emit('update turn');
}, 2500); 
