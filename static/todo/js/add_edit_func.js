function send_todo() {

    let xhr = new XMLHttpRequest();
    xhr.open("POST", "http://127.0.0.1:8000/todos/add");
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
