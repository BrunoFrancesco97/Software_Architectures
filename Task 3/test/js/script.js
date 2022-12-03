var position = 0;

function router(){
  switch (position) {
    case 0://Channel list
      document.querySelector("#go-back-button").style.display = "none";
      document.querySelector("#channel_container").style.display = "inline";
      document.querySelector("#course_container").style.display = "none";
      document.querySelector("#materials_container").style.display = "none";
      break;
    case 1: //Course list
    document.querySelector("#go-back-button").style.display = "inline";
      document.querySelector("#course_container").style.display = "inline";
      document.querySelector("#channel_container").style.display = "none";
      document.querySelector("#materials_container").style.display = "none";
      break;
    case 2: //Assignment list
    document.querySelector("#go-back-button").style.display = "inline";
      document.querySelector("#materials_container").style.display = "inline";
      document.querySelector("#course_container").style.display = "none";
      document.querySelector("#channel_container").style.display = "none";
      break;
  }
}




function get_courses(name) {
  position++;
  router();
  var request = new XMLHttpRequest();
  request.open("GET", "http://localhost:5000/channel/" + name, true);
  request.onreadystatechange = function () {
    if (request.status == 200 && request.readyState == 4) {
      obj = JSON.parse(request.responseText);
      console.log(obj);  
      for (let i = 0; i < obj.length; i++) {
        parent_div = document.querySelector("#course_template");
        //Remove all previous loaded channels
        element_to_delete = document.getElementsByClassName(
          "courses"
        );
        console.log(element_to_delete);
        for (let i = 0; i < parent_div.length; i++) {
          document.remove(element_to_delete[i]);
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
        document.querySelector("#course_container").appendChild(clone);
      }
    }
  };
  request.withCredentials = true;
  request.send();
}

function get_materials(name) {
  position++;
  router();
  var request = new XMLHttpRequest();
  request.open("GET", "http://localhost:5000/course/" + name, true);
  request.onreadystatechange = function () {
    if (request.status == 200 && request.readyState == 4) {
      obj = JSON.parse(request.responseText);
      files = obj.files;
      assignments_done = obj.assignment_done;
      assignments_remaining = obj.assignments_remaining;
      for (let i = 0; i < files.length; i++) {
        parent_div = document.querySelector("#file_template");
        //Remove all previous loaded channels
        element_to_delete = document.querySelector(
          "#file_template :not(.file_template)"
        );
        for (let i = 0; i < parent_div.length; i++) {
          parent_div[i].parentNode.removeChild(element_to_delete[i]);
        }
        //Clone div so to add new channels
        let clone = parent_div.cloneNode(true);
        clone.classList.remove("file_template");
        clone.style.visibility = "visible";
        let name = clone.getElementsByClassName("name");
        clone.setAttribute("id", files[i].name);
        name[0].innerText = files[i].name;
        document.querySelector("#files_container").appendChild(clone);
      }
      for (let i = 0; i < assignments_done.length; i++) {
        parent_div = document.querySelector("#assignments_done_template");
        //Remove all previous loaded channels
        element_to_delete = document.querySelector(
          "#assignments_done_template :not(.assignments_done_template)"
        );
        for (let i = 0; i < parent_div.length; i++) {
          parent_div[i].parentNode.removeChild(element_to_delete[i]);
        }
        //Clone div so to add new channels
        let clone = parent_div.cloneNode(true);
        clone.classList.remove("assignments_done_template");
        clone.style.visibility = "visible";
        let name = clone.getElementsByClassName("name");
        clone.setAttribute("id", assignments_done[i].name);
        name[0].innerText = assignments_done[i].name;
        document
          .querySelector("#assignments_done_container")
          .appendChild(clone);
      }
      for (let i = 0; i < assignments_remaining.length; i++) {
        parent_div = document.querySelector("#assignments_remaimning_template");
        //Remove all previous loaded channels
        element_to_delete = document.querySelector(
          "#assignments_remaimning_template :not(.assignments_remaimning_template)"
        );
        for (let i = 0; i < parent_div.length; i++) {
          parent_div[i].parentNode.removeChild(element_to_delete[i]);
        }
        //Clone div so to add new channels
        let clone = parent_div.cloneNode(true);
        clone.classList.remove("assignments_remaimning_template");
        clone.style.visibility = "visible";
        let name = clone.getElementsByClassName("name");
        clone.setAttribute("id", assignments_remaining[i].name);
        name[0].innerText = assignments_remaining[i].name;
        document
          .querySelector("#assignments_remaining_container")
          .appendChild(clone);
      }
    }
  };
  request.withCredentials = true;
  request.send();
}

function get_channels() {
  router();
  var request = new XMLHttpRequest();
  request.open("GET", "http://localhost:5000/channel", true);
  request.onreadystatechange = function () {
    if (request.status == 200 && request.readyState == 4) {
      obj = JSON.parse(request.responseText);
      for (let i = 0; i < obj.channels.length; i++) {
        parent_div = document.querySelector("#channel_template");
        //Remove all previous loaded channels
        element_to_delete = document.querySelector(
          "#channel_template :not(.channel_template)"
        );
        for (let i = 0; i < parent_div.length; i++) {
          parent_div[i].parentNode.removeChild(element_to_delete[i]);
        }
        //Clone div so to add new channels
        let clone = parent_div.cloneNode(true);
        clone.classList.remove("channel_template");
        clone.style.visibility = "visible";
        let name = clone.getElementsByClassName("name");
        let id = clone.getElementsByClassName("id");
        clone.setAttribute("id", obj.channels[i].id);
        name[0].innerText = obj.channels[i].name;
        id[0].innerText = obj.channels[i].id;
        document.querySelector("#channel_container").appendChild(clone);
      }
    }
  };
  request.withCredentials = true;
  request.send();
}
function goBack() {
  position--;
  router();
}
