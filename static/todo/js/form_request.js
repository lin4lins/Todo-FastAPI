function send_http_request(method, url, data = null) {

    var xhr = new XMLHttpRequest();
    xhr.open(method, url);
    xhr.setRequestHeader("Accept", "application/json");
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4) {
        var response = xhr.responseText;
        if (response == "null") {
            return;
        };

        var jsonResponse = JSON.parse(response);
        if  (xhr.status == 200 && jsonResponse.url) {
            window.location.replace(jsonResponse.url);
        }
        else {
            alert("Error is occurred. Reload page and try again");
        };
      }};

      if (data == null) {
        xhr.send();
        return;
      }

    xhr.send(JSON.stringify(data));
}

function get_todo_id_str_from_url() {
    var pathname = window.location.pathname;
    var re = /\d+/g;
    var found_array = pathname.match(re);
    var id = found_array[0];
    var todo_id_str = id.toString();
    return todo_id_str
}

function add_todo() {
    var method = "POST";
    var url = "/todos/add";

    var todo_data = {
      "title": document.getElementById("title").value,
      "description": document.getElementById("description").value,
      "priority": document.getElementById("priority").value
    };
    send_http_request(method, url, todo_data);
}

function edit_todo() {
    var method = "PUT";
    var todo_id_str = get_todo_id_str_from_url();
    var url = "/todos/edit"+"/"+todo_id_str;

    var todo_updated_data = {
      "title": document.getElementById("title").value,
      "description": document.getElementById("description").value,
      "priority": document.getElementById("priority").value
    };
    send_http_request(method, url, todo_updated_data);
}

function delete_todo() {
    var method = "DELETE";
    var todo_id_str = get_todo_id_str_from_url();
    var url = "/todos/delete"+"/"+todo_id_str;
    send_http_request(method, url);
}

function set_todo_complete(todo_id) {
    var method = "PUT";
    var url = "/todos/complete"+"/"+todo_id;

    var todo_status = {
        "completed": true
    };
    send_http_request(method, url, todo_status);
}

function login() {
    var method = "POST";
    var url = "/";
    var login_data = {
    "username": document.getElementById("username").value,
    "password": document.getElementById("password").value
    };

    send_http_request(method, url, login_data);
}