# group_project

Do `pip install -r requirements.txt` to  install
the requirements.


BACKEND TO FRONTEND
in flask
emit('name', {'msg':  any string}, room=game_code) sends to room
or
emit('name', {'msg':  any string}, session=session) sends to person

in js script
socket.on('name', function(data) {
    any js script
    to get values from dictionary use data.keyname
    in this case data.msg
});


FRONTEND TO BACKEND
in html (within /gameroom)
<div id=send> 
    shtuff
</div>

in js script
if the div is pressed
$('#send').click(function(e) {
    var text = 'pop'
    socket.emit('text', {msg: text});
});

in flask
@socketio.on('text', namespace='/gameroom')
def text_is_being_sent(data):
    game_code = session.get('game_code')
    username = session.get('username')
    
    game, player = check_in_game(game_code, username)
    if not game and not player:
        return False

    print(data['msg'])