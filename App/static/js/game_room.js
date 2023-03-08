var socket;
$(document).ready(function(){
    socket = io.connect('http://' + document.domain + ':' + location.port + '/gameroom');
    socket.on('connect', function() {
        socket.emit('join', {});
    });
    //Hides the roll-dice and buy
    $('#buy-property').hide();
    $('#buy-utility').hide();
    $('#dice-button').hide();
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
            $('#buy-property').show();
        } else {
            $('#buy-property').hide();
        };
    });
    //show or hide buy utility button
    socket.on('buy utility button change', function(data) {
        if(data.operation == 'show'){
            $('#buy-utility').show();
        } else {
            $('#buy-utility').hide();
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
    $('#roll-dice').click(function(data) {
        $('#dice-button').hide();
        socket.emit('roll dice');
    });
    //when the buy property box is pressed
    $('#buy-property').click(function(e) {
        $('#buy-property').hide();
        //const property = document.getElementById('property').value;
        socket.emit('buy-property');
    });
    //when the buy utility box is pressed
    $('#buy-utility').click(function(e) {
        $('#buy-utility').hide();
        //const property = document.getElementById('property').value;
        socket.emit('buy-utility');
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
//calls function every 2.5seconds
setInterval(function() {
    socket.emit('update turn');
}, 2500); 
