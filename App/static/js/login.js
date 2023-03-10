var socket;
$(document).ready(function() {
    socket = io.connect('http://' + document.domain + ':' + location.port + '/');
    $('#switch').click(function(e) {
        if ($('#login-header').html() == "Log In") {
            document.title = "Sign Up";
            $('#login-header').html("Sign Up");
            $('#submit').html("Sign Up");
            $('#submit').val("signup");
            $('#switch').html("Log In");
            $('#switch-p').html("Already have an account?");
        } else {
            document.title = "Log In";
            $('#login-header').html("Log In");
            $('#submit').html("Log In");
            $('#submit').val("login");
            $('#switch').html("Sign Up");
            $('#switch-p').html("Don't have an account?");
        }
    });
});