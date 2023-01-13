logged=false;
  if(!logged){
    display('login');
}


function display(page){
  console.log("Routing to: "+page);
  switch(page){
    case 'login':
      hide_home();
      hide_add_channel();
      hide_add_course();
      hide_channel();
      hide_course();
      show_login();
      break;
    case 'home':
      hide_login();
      show_homepage();
      show_home();
      break;
    case 'channel':
      hide_homepage();
      hide_add_course();
      hide_add_channel();
      hide_course();
      show_channel();
      break;
    case 'course':
      hide_homepage();
      hide_add_course();
      hide_add_channel();
      hide_channel();
      show_course();
      break;
    case 'add_channel':
      hide_homepage();
      hide_add_course();
      hide_channel();
      hide_course();
      show_add_channel();
      break;
    case 'add_course':
      hide_homepage();
      hide_add_channel();
      hide_channel();
      hide_course();
      show_add_course();
      break;
    default:
      console.log("Display page "+page+" error!");
      hide_login();
      hide_home();
      hide_channel();
      hide_course();
  }
}

function show_login(){
  $(document).prop('title','HR Admin | Log in');
  $('body').removeClass();
  $('body').addClass('login-page');
  $('body').addClass('hold-transition');
  $('#login').removeClass();
  $('#login').addClass('login-box');
}

function hide_login(){
  $('#login').addClass('d-none');
}

function show_home(){
  $(document).prop('title','HR Admin | Home');
  $('body').removeClass();
  $('body').addClass('sidebar-mini');
  $('#home').removeClass('d-none');

  getChannels();
}

function hide_home(){
  $('#home').addClass('d-none');
}

function show_add_channel(){
  $('#add_channel_wrapper').removeClass('d-none');
}

function show_add_course(){
  $('#add_course_wrapper').removeClass('d-none');
}

function hide_add_channel(){
  $('#add_channel_wrapper').addClass('d-none');
}

function hide_add_course(){
  $('#add_course_wrapper').addClass('d-none');
}

function show_homepage(){
  $('#home_wrapper').removeClass('d-none');
}

function hide_homepage(){
  $('#home_wrapper').addClass('d-none');
}

function show_channel(){
  $('#channel_wrapper').removeClass('d-none');
}

function hide_channel(){
  $('#channel_wrapper').addClass('d-none');
}

function show_course(){
  $('#course_wrapper').removeClass('d-none');
}

function hide_course(){
  $('#course_wrapper').addClass('d-none');
}