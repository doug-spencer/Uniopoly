var socket;
$(document).ready(function(){
    socket = io.connect('http://' + document.domain + ':' + location.port + '/gameroom');
    socket.on('connect', function() {
        socket.emit('join', {});
    });
    socket.on('status', function(data) {
        $('#messages').val($('#messages').val() + data.msg + '\n');
        $('#messages').scrollTop($('#messages')[0].scrollHeight);
    });
    socket.on('message', function(data) {
        $('#messages').val($('#messages').val() + data.msg + '\n');
        $('#messages').scrollTop($('#messages')[0].scrollHeight);
    });
    socket.on('roll dice button change', function(data) {
        if(data.operation == 'show'){
            $('#dice-button').show();
        } else {
            $('#dice-button').hide();
        };
    });
    socket.on('dice_roll', function(data) {
        document.getElementById('dice').innerHTML = 'dice value: ' + data.dice_value + ' new position: ' + data.position
        //$('dice').val('dice value: ' + data.dice_value + ' new position: ' + data.position);
    });
    $('#send').click(function(e) {
        text = $('#text').val();
        $('#text').val('');
        socket.emit('text', {msg: text});
    });
    $('#roll-dice').click(function(e) {
        socket.emit('roll dice');
    });
});
function leave_room() {
    socket.emit('left', {}, function() {
        socket.disconnect();
        window.location.href = "{{ url_for('index') }}";
    });
}
setInterval(function() {
    socket.emit('update turn');
}, 2500); //calls function every 2.5seconds