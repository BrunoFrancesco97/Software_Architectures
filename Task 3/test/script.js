function get_courses(name) {
  var request = new XMLHttpRequest();
  request.open("GET", "http://localhost:5000/channel/" + name, true);
  request.onreadystatechange = function () {
    if (request.status == 200 && request.readyState == 4) {
      obj = JSON.parse(request.responseText);

      for (let i = 0; i < obj.length; i++) {
        parent_div = document.querySelector("#course_template");
        //Remove all previous loaded channels
        element_to_delete = document.querySelector(
          "#course_template :not(.course_template)"
        );
        for (let i = 0; i < parent_div.length; i++) {
          parent_div[i].parentNode.removeChild(els[i]);
        }
        //Clone div so to add new channels
        let clone = parent_div.cloneNode(true);
        clone.classList.remove("course_template");
        clone.style.visibility = "visible";
        let name = clone.getElementsByClassName("name");
        let id = clone.getElementsByClassName("id");
        clone.setAttribute("id", obj[i].name);
        name[0].innerText = obj[i].name;
        id[0].innerText = obj[i].channel;
        console.log(clone)
        document.querySelector("#course_container").appendChild(clone);
        document.querySelector("#channel_container").style.display = 'none';
    }
    }
  };
  request.withCredentials = true;
  request.send();
}

function get_materials(name) {
    console.log(name);
    var request = new XMLHttpRequest();
    request.open("GET", "http://localhost:5000/course/" + name, true);
    request.onreadystatechange = function () {
        if (request.status == 200 && request.readyState == 4) {
        obj = JSON.parse(request.responseText);

        console.log(obj);
        }
    };
    request.withCredentials = true;
    request.send();
}
