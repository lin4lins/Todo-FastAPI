function login() {
    var method = "POST";
    var url = "/";
    var login_data = {
    "username": document.getElementById("username").value,
    "password": document.getElementById("password").value
    };

    send_http_request(method, url, login_data);
}

function logout() {
    var method = "POST";
    var url = "/logout";
    send_http_request(method, url);
}

function register() {
    var method = "POST";
    var url = "/signin";
    var signin_data = {
    "email": document.getElementById("email").value,
    "username": document.getElementById("username").value,
    "first_name": document.getElementById("first-name").value,
    "last_name": document.getElementById("last-name").value,
    "password": document.getElementById("password").value,
    "password2": document.getElementById("password2").value
    }

    send_http_request(method, url, signin_data);
}
