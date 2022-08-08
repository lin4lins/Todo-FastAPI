function send_todo(url) {

    let xhr = new XMLHttpRequest();
    xhr.open("POST", url);
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
            alert("Error is occurred by todo creation. Reload page and try again");
        };
      }};

    let data = {
      "title": document.getElementById("title").value,
      "description": document.getElementById("description").value,
      "priority": document.getElementById("priority").value
    };

    xhr.send(JSON.stringify(data));
}

function add_todo() {
    var url = "http://127.0.0.1:8000/todos/add";
    send_todo(url);
}

function edit_todo() {
    var todo_id = get_todo_id_from_url();
    var todo_id_str = todo_id.toString();
    var url = "http://127.0.0.1:8000/todos/edit"+"/"+todo_id_str;
    send_todo(url);
}

function delete_todo() {
    var todo_id = get_todo_id_from_url();
    var todo_id_str = todo_id.toString();
    var url = "http://127.0.0.1:8000/todos/delete"+"/"+todo_id_str;
    send_todo(url);
}


function get_todo_id_from_url() {
    var pathname = window.location.pathname;
    var re = /\d+/g;
    var found_array = pathname.match(re);
    var id = found_array[0];
    return id
}