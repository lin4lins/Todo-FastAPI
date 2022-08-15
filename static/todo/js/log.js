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

function is_user_logged_in() {
    if (document.cookie) {
        return true;
    }
    return false;
}