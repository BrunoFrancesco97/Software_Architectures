logged=false;
  if(!logged){
    display('login');
}


function display(page){
  console.log(page);
  switch(page){
    case 'login':
      hide_home();
      show_login();
      break;
    case 'home':
      hide_login();
      show_home();
      break;
    default:
      console.log("Display page ${page} error!")
      hide_login();
      hide_home();
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
}

function hide_home(){
  $('#home').addClass('d-none');
}