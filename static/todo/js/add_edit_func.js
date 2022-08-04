function myFunction() {

    let xhr = new XMLHttpRequest();
    xhr.open("POST", "http://127.0.0.1:8000/todos/add");
    xhr.setRequestHeader("Accept", "application/json");
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4) {
      if  (xhr.status == 200) {
        window.location.replace("/todos/read");
      }
        console.log(xhr.status);
        console.log(xhr.responseText);

      }};

    let data = {
      "title": document.getElementById("title").value,
      "description": document.getElementById("description").value,
      "priority": document.getElementById("priority").value
    };

    xhr.send(JSON.stringify(data));
}
