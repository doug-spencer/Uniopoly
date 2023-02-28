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
        window.location.href = "{{ url_for('index') }}";
    });
}

function buy_property() {
    const property = document.getElementById('property').value;
    socket.emit('buy property', {property: property});
    

    
}
//calls function every 2.5seconds
setInterval(function() {
    socket.emit('update turn');
}, 2500); 
