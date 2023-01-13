BASE_URL='http://localhost:5000/';

ENDPOINT_LOGIN='login';
ENDPOINT_LOGOUT='logout';
ENDPOINT_USER='user';
ENDPOINT_CHANNEL='channel';
ENDPOINT_COURSE='course';
ENDPOINT_ASSIGNMENT='assignment';

//login
function login(){
  if(is_form_valid()){
    $('#login_loading').removeClass('d-none');
    email=$('#email').val().replaceAll(' ', '');
    password=$('#password').val().replaceAll(' ', '');
    let hash = btoa(email+":"+password);
    var request = new XMLHttpRequest();
    request.open("GET", BASE_URL+ENDPOINT_LOGIN, true);
    request.onreadystatechange = function() {
      if(request.status == 200 && request.readyState == 4) {
        //obj = JSON.parse(request);
        console.log('login ok');

        var user_request = new XMLHttpRequest();
        user_request.open("GET", BASE_URL+ENDPOINT_USER, true);
        user_request.onreadystatechange = function() {
          if (request.status == 200 && request.readyState == 4 && !logged) {
            user_details = jQuery.parseJSON(user_request.response)
            console.log(user_details.user.role);
            if(user_details.user.role == "staff") {
              logged=true;
              display('home');
              $('#invalid_credentials').addClass('d-none');
              $('#login_loading').addClass('d-none');
              $('#email').removeClass('is-invalid');
              $('#password').removeClass('is-invalid');
            } else {
              $('#invalid_credentials').removeClass('d-none');
            }
          }
        }
        user_request.withCredentials = true;
        user_request.send();

      }else{
        $('#login_loading').addClass('d-none');
        $('#email').addClass('is-invalid');
        $('#password').addClass('is-invalid');
        $('#invalid_credentials').removeClass('d-none');
        //TODO: MOSTRARE ERRORE CREDENZIALI
      }
    };
    request.withCredentials = true;
    request.setRequestHeader("Authorization", "Basic "+hash);
    request.send();
  }
};

function register(){
  if(is_form_valid()){
    $('#login_loading').removeClass('d-none');
    let email=$('#email').val().replaceAll(' ', '');
    let password=$('#password').val().replaceAll(' ', '');

    let name = 'admin';
    let surname = 'admin';
    let role = 'staff';
    if(email != null && password != null && name != null && surname != null && role != null){
      email.replaceAll(' ', '');
      password.replaceAll(' ', '');
      name.replaceAll(' ', '');
      surname.replaceAll(' ', '');
      role.replaceAll(' ', '');
      if(email != "" && password != "" && name != "" && surname != "" && role != ""){
        var request = new XMLHttpRequest();
        request.open("POST", BASE_URL+ENDPOINT_LOGIN, true);
        request.setRequestHeader('Content-Type', 'application/json');
        request.onreadystatechange = function() {
          if(this.status == 200){
            $('#email').removeClass('is-invalid');
            $('#password').removeClass('is-invalid');
            $('#invalid_credentials').addClass('d-none');
            display('login');
          }else{
            $('#login_loading').addClass('d-none');
            $('#email').addClass('is-invalid');
            $('#password').addClass('is-invalid');
            $('#invalid_credentials').removeClass('d-none');
          }
        };
        //request.withCredentials = true;
        request.send(JSON.stringify({"email":email,"password":password,"name":name,"surname":surname,"role":role}));
      } 
    }
  }
  $('#login_loading').addClass('d-none');
  $('#email').addClass('is-invalid');
  $('#password').addClass('is-invalid');
  $('#invalid_credentials').removeClass('d-none');
}

function logout(){
  var request = new XMLHttpRequest();
  request.open("GET", BASE_URL+ENDPOINT_LOGOUT, true);
  request.onreadystatechange = function() {
  if(request.status == 200){
    logged=false;
    display('login');
  }
  };
  request.withCredentials = true;
  request.send();
  clean_home();
}

function getChannels() {
  var request = new XMLHttpRequest();
  request.open("GET", BASE_URL + ENDPOINT_CHANNEL, true);
  request.onreadystatechange = function () {
    if (request.status == 200 && request.readyState == 4) {
      channels = JSON.parse(request.responseText);
      console.log(channels);
      for (let i = 0; i < channels.channels.length; i++) {
        new_channel=$('#channel_template').clone().appendTo('#channel_menu');
        new_channel.prop('id', 'channel_'+channels.channels[i].name);
        new_channel.removeClass('d-none');
        new_channel_link = new_channel.children();
        new_channel_link.click({name: channels.channels[i].name}, getChannel);
        new_channel_label = new_channel.children().children()[1];
        new_channel_label.textContent = channels.channels[i].name;
      }
    }
  }
  request.withCredentials = true;
  request.send();
}

function clean_home() {
  $('#channel_menu').children().each(function() {
    if(($(this).attr('id') != 'channel_template') && ($(this).attr('id') != 'add_channel'))
    {
      console.log("removed: "+$(this).attr('id'));
      $(this).remove();
    }
  });
  $("#courses_menu").addClass("d-none");
  $("#courses_list").children().each(function() {
    if(($(this).attr('id') != 'course_template') && ($(this).attr('id') != 'add_course'))
    {
      console.log("removed: "+$(this).attr('id'));
      $(this).remove();
    }
  });
  $("#assignments_menu").addClass("d-none");
  $("#assignments_list").children().each(function() {
    if(($(this).attr('id') != 'assignment_template') && ($(this).attr('id') != 'add_assignment'))
    {
      console.log("removed: "+$(this).attr('id'));
      $(this).remove();
    }
  });
}

function clean_courses(){
  $("#courses_list").children().each(function() {
    if(($(this).attr('id') != 'course_template') && ($(this).attr('id') != 'add_course'))
    {
      console.log("removed: "+$(this).attr('id'));
      $(this).remove();
    }
  });
}

function clean_assignments() {
  $("#assignments_list").children().each(function() {
    if(($(this).attr('id') != 'assignment_template') && ($(this).attr('id') != 'add_assignment'))
    {
      console.log("removed: "+$(this).attr('id'));
      $(this).remove();
    }
  });
}

function getChannel(name) {
  var request = new XMLHttpRequest();
  request.open("GET", BASE_URL + ENDPOINT_CHANNEL + '/' + name.data.name, true);
  request.onreadystatechange = function () {
    if (request.status == 200 && request.readyState == 4) {
      courses = JSON.parse(request.responseText);
      console.log(courses.length);
      $("#current_channel").val(name.data.name);
      $("#current_delete_channel").val(name.data.name);
      $("#assignments_menu").addClass("d-none");
      clean_assignments();
      $("#courses_menu").addClass("d-none");
      clean_courses();

      for (let i = 0; i < courses.length; i++) {
        new_course=$('#course_template').clone().appendTo('#courses_list');
        new_course.prop('id', 'course_'+courses[i].name);
        new_course.prop('id', 'course_can');
        new_course.removeClass('d-none');
        new_course_link = new_course.children();
        new_course_link.click({name: courses[i].name}, getAssignments);
        console.log(courses[i].name);
        new_course_label = new_course.children().children()[1];
        new_course_label.textContent = courses[i].name;
      }
      $("#courses_menu").removeClass('d-none');
      //$("#channel_title").text(name.data.name);
      display('channel');
    }
  }
  request.withCredentials = true;
  request.send();
}

/*function getAssignments(name) {
  var request = new XMLHttpRequest();
  request.open("GET", BASE_URL + ENDPOINT_COURSE + '/' + name.data.name, true);
  request.onreadystatechange = function () {
    if (request.status == 200 && request.readyState == 4) {
      assignment = JSON.parse(request.responseText);
      console.log(assignment.assignment_done);
      console.log(assignment.assignments_remaining);

      $("#assignments_menu").addClass("d-none");
      clean_assignments();

      for (let i = 0; i < assignment.assignment_done.length; i++) {
        new_assignment=$('#assignment_template').clone().appendTo('#assignments_list');
        new_assignment.prop('id', 'course_'+assignment.assignment_done[i].name);
        new_assignment.prop('id', 'course_can');
        new_assignment.removeClass('d-none');
        new_assignment_link = new_assignment.children();
        new_assignment_link.click({name: assignment.assignments_remaining[i].name}, getAssignment);
        console.log(assignment.assignment_done[i].name);
        new_assignment_label = new_assignment.children().children()[1];
        new_assignment_label.textContent = assignment.assignment_done[i].name;
      }
      for (let i = 0; i < assignment.assignments_remaining.length; i++) {
        new_assignment=$('#assignment_template').clone().appendTo('#assignments_list');
        new_assignment.prop('id', 'course_'+assignment.assignments_remaining[i].name);
        new_assignment.prop('id', 'course_can');
        new_assignment.removeClass('d-none');
        new_assignment_link = new_assignment.children();
        new_assignment_link.click({name: assignment.assignments_remaining[i].name+" - feature to be developed.."}, getAssignment);
        console.log(assignment.assignments_remaining[i].name);
        new_assignment_label = new_assignment.children().children()[1];
        new_assignment_label.textContent = assignment.assignments_remaining[i].name;
      }
      $("#assignments_menu").removeClass('d-none');
    }
  }
  request.withCredentials = true;
  request.send();
}*/
function getAssignments(name) {
  $("#current_course").val(name.data.name);
  $("#current_delete_course").val(name.data.name);
  $("#assignments_menu").addClass("d-none");
  clean_assignments();
  //$("#courses_menu").addClass("d-none");
  //clean_courses();
  //$("#courses_menu").removeClass('d-none');
  //$("#channel_title").text(name.data.name);
  display('course');
}

function getAssignment(name){
  alert("feature no available!");
}

function add_channel(){
  display("add_channel");
}

function add_course(){
  display("add_course");
}

function addChannel(){
  var requestAC = new XMLHttpRequest();
  requestAC.open("POST", BASE_URL + ENDPOINT_CHANNEL, true);//http://localhost:5000/channel
  requestAC.setRequestHeader("Content-Type", "application/json;charset=UTF-8");//setting up CT header
  requestAC.onreadystatechange = function () {
    if (requestAC.status == 200 && requestAC.readyState == 4) {
      //add = JSON.parse(requestAC.responseText);
      ok=true;
      $("#channel_name").val('');
      setTimeout(function() { clean_home(); getChannels(); }, 1000);
      toastr.info("Channel added!");//toast ok
    } else {
      if(requestAC.status != 200) {
        toastr.error("something went wrong");//toast ko
      }
    }
  }
  requestAC.withCredentials = true;
  requestAC.send(JSON.stringify({ "channel": $("#channel_name").val() }));//log new channel json
}

function addCourse(){
  var requestAC = new XMLHttpRequest();
  requestAC.open("POST", BASE_URL + ENDPOINT_COURSE, true);//http://localhost:5000/course
  requestAC.setRequestHeader("Content-Type", "application/json;charset=UTF-8");//setting up CT header
  requestAC.onreadystatechange = function () {
    if (requestAC.status == 200 && requestAC.readyState == 4) {
      //add = JSON.parse(requestAC.responseText);
      $("#course_name").val('');
      setTimeout(function() { clean_home(); getChannels(); }, 1000);
      toastr.info("Course added!");//toast ok
    } else {
      if(requestAC.status != 200){
        toastr.error("something went wrong");//toast ko
      }
    }
  }
  requestAC.withCredentials = true;
  requestAC.send(JSON.stringify({ "channel": $("#current_channel").val(), "course": $("#course_name").val() }));//log new channel json
}

function deleteChannel(){
  var requestAC = new XMLHttpRequest();
  requestAC.open("DELETE", BASE_URL + ENDPOINT_CHANNEL, true);//http://localhost:5000/channel
  requestAC.setRequestHeader("Content-Type", "application/json;charset=UTF-8");//setting up CT header
  requestAC.onreadystatechange = function () {
    if (requestAC.status == 200 && requestAC.readyState == 4) {
      //add = JSON.parse(requestAC.responseText);
      //$("#channel_name").val('');
      setTimeout(function() { clean_home(); getChannels(); }, 1000);
      toastr.info("Channel deleted!");//toast ok
      clean_home();
      display('home');
    } else {
      if(requestAC.status != 200){
        toastr.error("something went wrong");//toast ko
      }
    }
  }
  requestAC.withCredentials = true;
  requestAC.send(JSON.stringify({ "channel": $("#current_channel").val() }));//log new channel json
}

function deleteCourse(){
  var requestAC = new XMLHttpRequest();
  requestAC.open("DELETE", BASE_URL + ENDPOINT_COURSE, true);//http://localhost:5000/course
  requestAC.setRequestHeader("Content-Type", "application/json;charset=UTF-8");//setting up CT header
  requestAC.onreadystatechange = function () {
    if (requestAC.status == 200 && requestAC.readyState == 4) {
      //add = JSON.parse(requestAC.responseText);
      ok=true;
      $("#current_delete_course").val('');
      setTimeout(function() { clean_home(); getChannels(); }, 1000);
      toastr.info("Course deleted!");//toast ok
      clean_home();
      display('home');
    } else {
      if(requestAC.status != 200){
        toastr.error("something went wrong");//toast ko
      }
    }
  }
  requestAC.withCredentials = true;
  requestAC.send(JSON.stringify({ "channel": $("#current_channel").val(), "course": $("#current_delete_course").val() }));//log new channel json
}