var position = 0;

function router() {
  switch (position) {
    case 0: //Channel list
      document.querySelector("#go-back-button").classList.add("d-none");
      document.querySelector("#channel_container").classList.remove("d-none");
      document.querySelector("#course_container").classList.add("d-none");
      document.querySelector("#materials_container").classList.add("d-none");
      document.querySelector("#exercise_container").classList.add("d-none");
      document.querySelector("#user_container").classList.add("d-none");
      document.querySelector("#previous_container").classList.add("d-none");
      break;
    case 1: //Course list
      document.querySelector("#go-back-button").classList.remove("d-none");
      document.querySelector("#course_container").classList.remove("d-none");
      document.querySelector("#channel_container").classList.add("d-none");
      document.querySelector("#materials_container").classList.add("d-none");
      document.querySelector("#exercise_container").classList.add("d-none");
      document.querySelector("#user_container").classList.add("d-none");
      document.querySelector("#previous_container").classList.add("d-none");
      break;
    case 2: //Assignment list
      document.querySelector("#go-back-button").classList.remove("d-none");
      document.querySelector("#materials_container").classList.remove("d-none");
      document.querySelector("#course_container").classList.add("d-none");
       document.querySelector("#channel_container").classList.add("d-none");
      document.querySelector("#exercise_container").classList.add("d-none");
      document.querySelector("#user_container").classList.add("d-none");
      document.querySelector("#previous_container").classList.add("d-none");
      break;
    case 3: //Assignment content
      document.querySelector("#go-back-button").classList.remove("d-none");
      document.querySelector("#materials_container").classList.add("d-none");
      document.querySelector("#course_container").classList.add("d-none");
       document.querySelector("#channel_container").classList.add("d-none");
      document.querySelector("#user_container").classList.add("d-none");
      document.querySelector("#exercise_container").classList.remove("d-none");
      document.querySelector("#previous_container").classList.add("d-none");
      break;
    case 4:
      document.querySelector("#go-back-button").classList.remove("d-none");
       document.querySelector("#channel_container").classList.add("d-none");
      document.querySelector("#course_container").classList.add("d-none");
      document.querySelector("#materials_container").classList.add("d-none");
      document.querySelector("#exercise_container").classList.add("d-none");
      document.querySelector("#user_container").classList.remove("d-none");
      document.querySelector("#previous_container").classList.add("d-none");
      break;
    case 5:
      document.querySelector("#go-back-button").classList.remove("d-none");
       document.querySelector("#channel_container").classList.add("d-none");
      document.querySelector("#course_container").classList.add("d-none");
      document.querySelector("#materials_container").classList.add("d-none");
      document.querySelector("#exercise_container").classList.add("d-none");
      document.querySelector("#user_container").classList.add("d-none");
      document.querySelector("#previous_container").classList.remove("d-none");
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
      clone.classList.remove("d-none");
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

function get_courses(el) {
  var request = new XMLHttpRequest();
  let name = el.getElementsByClassName('name')[0].innerText;
  request.open("GET", "http://localhost:5000/channel/" + name, true);
  request.onreadystatechange = function () {
    if (request.status == 200 && request.readyState == 4) {
      localStorage.setItem('channel',name);
      position = 1;
      router();
      obj = JSON.parse(request.responseText);
      //Remove all previous loaded channels
      document.querySelectorAll(".courses").forEach((el) => el.remove());
      channel_name = localStorage.getItem('channel');
      document.getElementById('channel_name_course').innerText = channel_name;
      for (let i = 0; i < obj.length; i++) {
        parent_div = document.querySelector("#course_template");
        parent_div.getElementsByClassName('boxx')[0].setAttribute('name',obj[i].name)
        //Clone div so to add new channels
        let clone = parent_div.cloneNode(true);
        clone.classList.add("courses");
        clone.classList.remove("course_template");
        clone.classList.remove("d-none");
        clone.setAttribute('title',  obj[i].name);
        let name = clone.getElementsByClassName("name");
        let id = clone.getElementsByClassName("id");
        clone.setAttribute("id", obj[i].name);
        name[0].innerText = obj[i].name;
        id[0].innerText = obj[i].channel;
        document.querySelector("#course_container").appendChild(clone);
      }
    }else{
      if(request.status == 401 && request.readyState == 4){
        toggleToast("You aren't subscribed to this channel");
        showModalCh(name);
      }
    }
  };
  request.withCredentials = true;
  request.send();
}

function subscribeChannel(channel){
  let name = channel.parentNode.parentNode.parentNode.parentNode.getAttribute('name');
  var request = new XMLHttpRequest();
  request.open("POST", "http://localhost:5000/channel_subscription", true);
  request.setRequestHeader('Content-Type', 'application/json');
  request.onreadystatechange = function () {
    if (request.status == 200 && request.readyState == 4) {
      closeModalCh();
    }
  };
  request.withCredentials = true;
  request.send(JSON.stringify({"channel":name}));
}

function deletesubscribeChannel(channel){
  let name = channel.parentNode.parentNode.parentNode.parentNode.getAttribute('name');
  var request = new XMLHttpRequest();
  request.open("DELETE", "http://localhost:5000/channel_subscription", true);
  request.setRequestHeader('Content-Type', 'application/json');
  request.onreadystatechange = function () {
    if (request.status == 200 && request.readyState == 4) {
      closeModalCh();
    }
  };
  request.withCredentials = true;
  request.send(JSON.stringify({"channel":name}));
}

function subscribeCourse(el){
  let name = el.parentNode.parentNode.parentNode.parentNode.getAttribute('name');
  var request = new XMLHttpRequest();
  request.open("POST", "http://localhost:5000/course_subscription", true);
  request.setRequestHeader('Content-Type', 'application/json');
  request.onreadystatechange = function () {
    if (request.status == 200 && request.readyState == 4) {
      closeModalCh2();
    }
  };
  request.withCredentials = true;
  request.send(JSON.stringify({"course":name}));
}

function deletesubscribeCourse(el){
  let name = el.parentNode.parentNode.parentNode.parentNode.getAttribute('name');
  console.log(name);
  var request = new XMLHttpRequest();
  request.open("DELETE", "http://localhost:5000/course_subscription", true);
  request.setRequestHeader('Content-Type', 'application/json');
  request.onreadystatechange = function () {
    if (request.status == 200 && request.readyState == 4) {
      closeModalCh2();
    }
  };
  request.withCredentials = true;
  request.send(JSON.stringify({"course":name}));
}


function get_materials(name) {
  let request = new XMLHttpRequest();
  request.open("GET", "http://localhost:5000/course/" + name, true);
  request.onreadystatechange = function () {
    if (request.status == 200 && request.readyState == 4) {
      position = 2;
      router();
      document.querySelector("#go-back-button").classList.add('d-none');
      document.getElementById("course_name").innerText = name;
      obj = JSON.parse(request.responseText);
      files = obj.files;
      assignments_done = obj.assignment_done;
      assignments_remaining = obj.assignments_remaining;
      document.querySelectorAll(".files").forEach((el) => el.remove());
      for (let i = 0; i < files.length; i++) {
        parent_div = document.querySelector("#file_template");
        let clone = parent_div.cloneNode(true);
        clone.classList.add("files");
        clone.classList.remove("file_template");
        clone.classList.remove("d-none");
        let name = clone.getElementsByClassName("name");
        name[0].setAttribute("title", files[i].name);
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
        clone.classList.remove("d-none");
        let name = clone.getElementsByClassName("name");
        name[0].setAttribute("title", assignments_done[i].name);
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
        clone.classList.remove("d-none");
        let name = clone.getElementsByClassName("name");
        let deadline = clone.getElementsByClassName("deadline");
        clone.setAttribute("id", assignments_remaining[i].id);
        name[0].setAttribute("title", assignments_remaining[i].name);
        name[0].innerText = assignments_remaining[i].name;
        deadline[0].innerText = assignments_remaining[i].deadline;
        document
          .querySelector("#assignments_remaining_container")
          .appendChild(clone);
      }
    } else {
      if(request.status == 401 && request.readyState == 4){
        toggleToast("You aren't subscribed to this course!");
      showModalCh2(name);
      }
    }
  };
  request.withCredentials = true;
  request.send();
}

function get_channels() {
  var request = new XMLHttpRequest();
  request.open("GET", "http://localhost:5000/channel", true);
  let body_loader =  document.getElementById("body-content");
  let loader =  document.getElementById("loader");
  body_loader.style.opacity = "0";
  loader.classList.remove("d-none");
  request.onreadystatechange = function () {
    if (request.status == 200 && request.readyState == 4) {
      body_loader.style.opacity = "1";
      loader.classList.add("d-none");
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
        clone.classList.remove("d-none");
        clone.setAttribute('title',  obj.channels[i].name);
        let name = clone.getElementsByClassName("name");
        let id = clone.getElementsByClassName("id");
        clone.setAttribute("id", obj.channels[i].id);
        name[0].innerText = obj.channels[i].name;
        id[0].innerText = obj.channels[i].id;
        document.querySelector("#channel_container").appendChild(clone);
      }
    } else {
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
      //Remove all previous loaded exercises
      document.querySelectorAll(".exercises").forEach((el) => el.remove());
      document.querySelectorAll(".results").forEach((el) => el.remove());
      document.querySelector("#send_button").classList.remove("d-none");
      for (let i = 0; i < obj.exercises.length; i++) {
        parent_div = document.querySelector("#exercise_template");
        //Clone div so to add new exercise
        let clone = parent_div.cloneNode(true);
        clone.classList.add("exercises");
        clone.classList.remove("exercise_template");
        clone.classList.remove("d-none");
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
      //Remove all previous loaded exercises
      document.querySelectorAll(".results_prev").forEach((el) => el.remove());
      parent_div = document.querySelector("#final_template2");
      //Clone div so to add new exercise
      let clone = parent_div.cloneNode(true);
      clone.classList.add("results_prev");
      clone.classList.remove("final_template2");
      clone.classList.remove("d-none");
      let nameD = clone.getElementsByClassName("final_template_name2");
      let sub = clone.getElementsByClassName("final_template_subscription2");
      let comment = clone.getElementsByClassName("final_template_comment2");
      let score = clone.getElementsByClassName("final_template_result2");
      nameD[0].innerText = nameDiv;
      sub[0].innerText = obj.result[0].subscription;
      if(obj.result[0].comment == null){
        comment[0].innerText = "No comment";
      }else{
        score[0].innerText = obj.result[0].comment;
      }
      score[0].innerText = obj.result[0].result+"/100";    
      document.querySelector("#previous_container").appendChild(clone);
    }
  };
  request.withCredentials = true;
  request.send();
}
function send_solution(el) {
  information = el.parentNode.parentNode;
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
  document.querySelector("#send_button").classList.add("d-none");
  let body_loader =  document.querySelector("#body-content");
  let loader =  document.querySelector("#loader");
  body_loader.style.opacity = "0";
  loader.classList.remove("d-none");
  pp = document.querySelectorAll(".exercises");
  for(let z = 0; z < pp.length; z++){
    pp[z].classList.add("d-none");
  }
  let request = new XMLHttpRequest();
  request.open("PUT", "http://localhost:5000/exercise", true);
  request.onreadystatechange = function () {
    if (request.status == 200 && request.readyState == 4) {
      obj = JSON.parse(request.responseText);
      document.querySelectorAll(".results").forEach((el) => el.remove());
      if (obj.results != null && obj.results.length == 1) {
        body_loader.style.opacity = "1";
        loader.classList.add("d-none");
        result_div = document.querySelector("#results_template");
        let clone = result_div.cloneNode(true);
        clone.classList.remove("results_template");
        clone.classList.add("results");
        final = clone.getElementsByClassName("final_template");
        final[0].getElementsByClassName(
          "final_template_subscription"
        )[0].innerText = obj.results[0].subscription;
        if(obj.results[0].comment == null){
          final[0].getElementsByClassName("final_template_comment")[0].innerText = "No comment";
        }else{
          final[0].getElementsByClassName("final_template_comment")[0].innerText =
          obj.results[0].comment;
        }
        
        final[0].getElementsByClassName("final_template_result")[0].innerText =
          obj.results[0].result+"/100";
        let actual = clone.getElementsByClassName("this_template");
        if(obj.error == null || obj.error == ""){
          actual[0].getElementsByClassName("this_template_error")[0].innerText = "No error";
        }else{
          actual[0].getElementsByClassName("this_template_error")[0].innerText =
          obj.error;
        }
        
        actual[0].getElementsByClassName("this_template_similar")[0].innerText =
          obj.similar_responses;
        tests_container = actual[0].querySelector("#this_template_container");
        //actual[0].getElementsByClassName("this_template_correct")[0].innerText = obj.results[0].result;
        for (let i = 0; i < obj.tests.length; i++) {
          let test = obj.tests[i];
          let test_view =
            tests_container.getElementsByClassName("this_template_test");
          let clone2 = test_view[0].cloneNode(true);
          clone2.classList.remove("d-none");
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
        clone.classList.remove("d-none");
        pp = document.querySelectorAll(".exercises");
        for(let z = 0; z < pp.length; z++){
          pp[z].classList.add("d-none");
        }
        document.querySelector("#exercise_container").appendChild(clone);
      }
    }else{
      body_loader.style.opacity = "1";
      loader.classList.add("d-none");
      pp = document.querySelectorAll(".exercises");
      for(let z = 0; z < pp.length; z++){
        pp[z].classList.remove("d-none");
      }
    }
  };
  request.withCredentials = true;
  request.send(formData);
}

function toggleMenu(){
  if(document.getElementById('menu_dialog_container').classList.contains('d-none')){
    document.getElementById('menu_dialog_container').classList.remove('d-none');
  }else{
    document.getElementById('menu_dialog_container').classList.add('d-none');
  }
}

function toggleToast(text) {
  el = document.querySelector('#toast_made');
  el.classList.remove('d-none');
  el2 =  document.querySelector('#toast_made_message');  
  el2.innerText = text;
  setTimeout(function(){
    el.classList.add('d-none');
  },4000)
}


function showModalCh(name){
  document.getElementById('modal_made').classList.remove('d-none');
  document.getElementById('modal_made').setAttribute('name',name);
}
function closeModalCh(){
  document.getElementById('modal_made').classList.add('d-none');
}
function showModalCh2(name){
  document.getElementById('modal_made2').classList.remove('d-none');
  document.getElementById('modal_made2').setAttribute('name',name);
}
function closeModalCh2(){
  document.getElementById('modal_made2').classList.add('d-none');
}

document.addEventListener("click",function(event){
  var div = document.getElementById("menuicon");
  if(div != event.target){
    document.getElementById('menu_dialog_container').classList.add('d-none');
  }
});