var position = 0;

function router() {
  console.log(position);
  switch (position) {
    case 0: //Channel list
      document.querySelector("#go-back-button").style.display = "none";
      document.querySelector("#go-user-button").style.display = "inline";
      document.querySelector("#channel_container").style.display = "inline";
      document.querySelector("#course_container").style.display = "none";
      document.querySelector("#materials_container").style.display = "none";
      document.querySelector("#exercise_container").style.display = "none";
      document.querySelector("#user_container").style.display = "none";
      document.querySelector("#previous_container").style.display = "none";
      break;
    case 1: //Course list
      document.querySelector("#go-back-button").style.display = "inline";
      document.querySelector("#go-user-button").style.display = "none";
      document.querySelector("#course_container").style.display = "inline";
      document.querySelector("#channel_container").style.display = "none";
      document.querySelector("#materials_container").style.display = "none";
      document.querySelector("#exercise_container").style.display = "none";
      document.querySelector("#user_container").style.display = "none";
      document.querySelector("#previous_container").style.display = "none";
      break;
    case 2: //Assignment list
      document.querySelector("#go-back-button").style.display = "inline";
      document.querySelector("#go-user-button").style.display = "none";
      document.querySelector("#materials_container").style.display = "inline";
      document.querySelector("#course_container").style.display = "none";
      document.querySelector("#channel_container").style.display = "none";
      document.querySelector("#exercise_container").style.display = "none";
      document.querySelector("#user_container").style.display = "none";
      document.querySelector("#previous_container").style.display = "none";
      break;
    case 3: //Assignment content
      document.querySelector("#go-back-button").style.display = "inline";
      document.querySelector("#go-user-button").style.display = "none";
      document.querySelector("#materials_container").style.display = "none";
      document.querySelector("#course_container").style.display = "none";
      document.querySelector("#channel_container").style.display = "none";
      document.querySelector("#user_container").style.display = "none";
      document.querySelector("#exercise_container").style.display = "inline";
      document.querySelector("#previous_container").style.display = "none";
      break;
    case 4:
      document.querySelector("#go-back-button").style.display = "inline";
      document.querySelector("#go-user-button").style.display = "none";
      document.querySelector("#channel_container").style.display = "none";
      document.querySelector("#course_container").style.display = "none";
      document.querySelector("#materials_container").style.display = "none";
      document.querySelector("#exercise_container").style.display = "none";
      document.querySelector("#user_container").style.display = "inline";
      document.querySelector("#previous_container").style.display = "none";
      break;
    case 5:
      document.querySelector("#go-back-button").style.display = "inline";
      document.querySelector("#go-user-button").style.display = "none";
      document.querySelector("#channel_container").style.display = "none";
      document.querySelector("#course_container").style.display = "none";
      document.querySelector("#materials_container").style.display = "none";
      document.querySelector("#exercise_container").style.display = "none";
      document.querySelector("#user_container").style.display = "none";
      document.querySelector("#previous_container").style.display = "inline";
      break;
  }
}

function goUser() {
  let request = new XMLHttpRequest();
  request.open("GET", "http://localhost:5000/user", true);
  request.onreadystatechange = function () {
    if (request.status == 200 && request.readyState == 4) {
      position = 4;
      router();
      obj = JSON.parse(request.responseText);
      //Remove all previous loaded users
      document.querySelectorAll(".users").forEach((el) => el.remove());
      parent_div = document.querySelector("#user_template");
      //Clone div so to add new user
      let clone = parent_div.cloneNode(true);
      clone.classList.add("users");
      clone.classList.remove("user_template");
      clone.style.visibility = "visible";
      let name = clone.getElementsByClassName("name");
      let surname = clone.getElementsByClassName("surname");
      let email = clone.getElementsByClassName("email");
      let role = clone.getElementsByClassName("role");
      let creation = clone.getElementsByClassName("creation");
      name[0].innerText = obj.user.name;
      surname[0].innerText = obj.user.surname;
      email[0].innerText = obj.user.email;
      role[0].innerText = obj.user.role;
      creation[0].innerText = obj.user.creation;
      document.querySelector("#user_container").appendChild(clone);
    }
  };
  request.withCredentials = true;
  request.send();
}

function get_courses(name) {
  var request = new XMLHttpRequest();
  request.open("GET", "http://localhost:5000/channel/" + name, true);
  request.onreadystatechange = function () {
    if (request.status == 200 && request.readyState == 4) {
      position = 1;
      router();
      obj = JSON.parse(request.responseText);
      //Remove all previous loaded channels
      document.querySelectorAll(".courses").forEach((el) => el.remove());
      for (let i = 0; i < obj.length; i++) {
        parent_div = document.querySelector("#course_template");
        //Clone div so to add new channels
        let clone = parent_div.cloneNode(true);
        clone.classList.add("courses");
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
  var request = new XMLHttpRequest();
  request.open("GET", "http://localhost:5000/course/" + name, true);
  request.onreadystatechange = function () {
    if (request.status == 200 && request.readyState == 4) {
      position = 2;
      router();
      document.getElementById("course_name").innerText = name;
      obj = JSON.parse(request.responseText);
      files = obj.files;
      assignments_done = obj.assignment_done;
      assignments_remaining = obj.assignments_remaining;
      console.log(assignments_remaining);
      document.querySelectorAll(".files").forEach((el) => el.remove());
      for (let i = 0; i < files.length; i++) {
        parent_div = document.querySelector("#file_template");
        let clone = parent_div.cloneNode(true);
        clone.classList.add("files");
        clone.classList.remove("file_template");
        clone.style.visibility = "visible";
        let name = clone.getElementsByClassName("name");
        clone.setAttribute("id", files[i].name);
        name[0].innerText = files[i].name;
        document.querySelector("#files_container").appendChild(clone);
      }
      document
        .querySelectorAll(".assignments_done")
        .forEach((el) => el.remove());
      for (let i = 0; i < assignments_done.length; i++) {
        parent_div = document.querySelector("#assignments_done_template");
        let clone = parent_div.cloneNode(true);
        clone.classList.add("assignments_done");
        clone.classList.remove("assignments_done_template");
        clone.style.visibility = "visible";
        let name = clone.getElementsByClassName("name");
        clone.setAttribute("id", assignments_done[i].id);
        name[0].innerText = assignments_done[i].name;
        document
          .querySelector("#assignments_done_container")
          .appendChild(clone);
      }
      document
        .querySelectorAll(".assignments_remaining")
        .forEach((el) => el.remove());
      for (let i = 0; i < assignments_remaining.length; i++) {
        parent_div = document.querySelector("#assignments_remaimning_template");
        //Clone div so to add new channels
        let clone = parent_div.cloneNode(true);
        clone.classList.add("assignments_remaining");
        clone.classList.remove("assignments_remaimning_template");
        clone.style.visibility = "visible";
        let name = clone.getElementsByClassName("name");
        let deadline = clone.getElementsByClassName("deadline");
        clone.setAttribute("id", assignments_remaining[i].id);
        name[0].innerText = assignments_remaining[i].name;
        deadline[0].innerText = assignments_remaining[i].deadline;
        document
          .querySelector("#assignments_remaining_container")
          .appendChild(clone);
      }
    } else {
      position--;
      router();
    }
  };
  request.withCredentials = true;
  request.send();
}

function get_channels() {
  var request = new XMLHttpRequest();
  request.open("GET", "http://localhost:5000/channel", true);
  request.onreadystatechange = function () {
    if (request.status == 200 && request.readyState == 4) {
      position = 0;
      router();
      obj = JSON.parse(request.responseText);
      //Remove all previous loaded channels
      document.querySelectorAll(".channels").forEach((el) => el.remove());
      for (let i = 0; i < obj.channels.length; i++) {
        parent_div = document.querySelector("#channel_template");
        //Clone div so to add new channels
        let clone = parent_div.cloneNode(true);
        clone.classList.add("channels");
        clone.classList.remove("channel_template");
        clone.style.visibility = "visible";
        let name = clone.getElementsByClassName("name");
        let id = clone.getElementsByClassName("id");
        clone.setAttribute("id", obj.channels[i].id);
        name[0].innerText = obj.channels[i].name;
        id[0].innerText = obj.channels[i].id;
        document.querySelector("#channel_container").appendChild(clone);
      }
    } else {
      console.log(request.status);
      if (request.status == 0) {
        window.location.replace("index.html");
      }
    }
  };
  request.withCredentials = true;
  request.send();
}
function goBack() {
  if (position != 4) {
    position--;
    if ((position == 4)) {
      position = 2;
    }
    if (position == 2) {
      let name = document.getElementById("course_name").innerText;
      get_materials(name);
      position--;
    }
  } else {
    position = 0;
  }
  router();
}

function compute(el) {
  let nameDiv = el.getElementsByClassName("name")[0].innerText;
  document.getElementsByClassName("content_title")[0].innerText = nameDiv;
  let idDiv = el.getAttribute("id");
  let request = new XMLHttpRequest();
  request.open("GET", "http://localhost:5000/exercise/" + idDiv, true);
  //request.setRequestHeader('Content-Type', 'application/json');
  request.onreadystatechange = function () {
    if (request.status == 200 && request.readyState == 4) {
      position = 3;
      router();
      obj = JSON.parse(request.responseText);
      console.log(obj);
      //Remove all previous loaded exercises
      document.querySelectorAll(".exercises").forEach((el) => el.remove());
      document.querySelectorAll(".results").forEach((el) => el.remove());
      document.querySelector("#send_button").style.display = "inline";
      for (let i = 0; i < obj.exercises.length; i++) {
        parent_div = document.querySelector("#exercise_template");
        //Clone div so to add new exercise
        let clone = parent_div.cloneNode(true);
        clone.classList.add("exercises");
        clone.classList.remove("exercise_template");
        clone.style.display = "inline";
        let quest = clone.getElementsByClassName("content_quest");
        let type = clone.getElementsByClassName("content_type");
        let id = clone.getElementsByClassName("content_id");
        let assignment = clone.getElementsByClassName("content_assignment");
        clone.setAttribute("id", obj.exercises[i].id);
        quest[0].innerText = obj.exercises[i].quest;
        type[0].innerText = obj.exercises[i].type;
        id[0].innerText = obj.exercises[i].id;
        assignment[0].innerText = obj.exercises[i].assignment;
        document.querySelector("#exercise_container").appendChild(clone);
      }
    }
  };
  request.withCredentials = true;
  request.send();
}
function seePrevious(el) {
  let nameDiv = el.getElementsByClassName("name")[0].innerText;
  document.getElementsByClassName("content_title")[0].innerText = nameDiv;
  let idDiv = el.getAttribute("id");
  let request = new XMLHttpRequest();
  request.open("GET", "http://localhost:5000/result/" + idDiv, true);
  //request.setRequestHeader('Content-Type', 'application/json');
  request.onreadystatechange = function () {
    if (request.status == 200 && request.readyState == 4) {
      position = 5;
      router();
      obj = JSON.parse(request.responseText);
      console.log(obj);
      //Remove all previous loaded exercises
      document.querySelectorAll(".results_prev").forEach((el) => el.remove());
      parent_div = document.querySelector("#final_template2");
      //Clone div so to add new exercise
      let clone = parent_div.cloneNode(true);
      clone.classList.add("results_prev");
      clone.classList.remove("final_template2");
      clone.style.display = "inline";
      let sub = clone.getElementsByClassName("final_template_subscription2");
      let comment = clone.getElementsByClassName("final_template_comment2");
      let score = clone.getElementsByClassName("final_template_result2");
      sub[0].innerText = obj.result[0].subscription;
      comment[0].innerText = obj.result[0].comment;
      score[0].innerText = obj.result[0].result;
      document.querySelector("#previous_container").appendChild(clone);
    }
  };
  request.withCredentials = true;
  request.send();
}
function send_solution(el) {
  information = el.parentNode;
  let type = information.getElementsByClassName("content_type")[0].innerText;
  let select = information.getElementsByClassName("content_language")[0];
  let language = select.options[select.selectedIndex].value;
  let exercise = information.getElementsByClassName("content_id")[0].innerText;
  let program = information.getElementsByClassName("text_program")[0].value;
  let file = information.getElementsByClassName("content_file")[0].files[0];
  let formData = new FormData();
  formData.append("type", type);
  formData.append("text", program);
  formData.append("language", language);
  formData.append("exercise", exercise);
  formData.append("file", file);
  document.querySelector("#send_button").style.display = "none";
  let request = new XMLHttpRequest();
  request.open("PUT", "http://localhost:5000/exercise", true);
  request.onreadystatechange = function () {
    if (request.status == 200 && request.readyState == 4) {
      obj = JSON.parse(request.responseText);
      console.log(obj);
      document.querySelectorAll(".results").forEach((el) => el.remove());
      if (obj.results != null && obj.results.length == 1) {
        result_div = document.querySelector("#results_template");
        let clone = result_div.cloneNode(true);
        clone.classList.remove("results_template");
        clone.classList.add("results");
        final = clone.getElementsByClassName("final_template");
        final[0].getElementsByClassName(
          "final_template_subscription"
        )[0].innerText = obj.results[0].subscription;
        final[0].getElementsByClassName("final_template_comment")[0].innerText =
          obj.results[0].comment;
        final[0].getElementsByClassName("final_template_result")[0].innerText =
          obj.results[0].result;
        let actual = clone.getElementsByClassName("this_template");
        actual[0].getElementsByClassName("this_template_error")[0].innerText =
          obj.error;
        actual[0].getElementsByClassName("this_template_similar")[0].innerText =
          obj.similar_responses;
        tests_container = actual[0].querySelector("#this_template_container");
        //actual[0].getElementsByClassName("this_template_correct")[0].innerText = obj.results[0].result;
        for (let i = 0; i < obj.tests.length; i++) {
          let test = obj.tests[i];
          let test_view =
            tests_container.getElementsByClassName("this_template_test");
          let clone2 = test_view[0].cloneNode(true);
          clone2.getElementsByClassName(
            "this_template_test_quest"
          )[0].innerText = test[3];
          clone2.getElementsByClassName(
            "this_template_test_result"
          )[0].innerText = test[0];
          clone2.getElementsByClassName(
            "this_template_test_expected"
          )[0].innerText = test[2];
          clone2.getElementsByClassName("this_template_given")[0].innerText =
            test[1];
          tests_container.appendChild(clone2);
        }
        clone.style.display = "inline";
        document.querySelector("#exercise_container").appendChild(clone);
      }
    }
  };
  request.withCredentials = true;
  request.send(formData);
}
