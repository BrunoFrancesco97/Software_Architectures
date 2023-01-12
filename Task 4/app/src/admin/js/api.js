BASE_URL='http://localhost:5000/';

ENDPOINT_LOGIN='login';
ENDPOINT_LOGOUT='logout';
ENDPOINT_USER='user';
ENDPOINT_CHANNEL='channel';

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
            if(user_details.user.role == "admin") {
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
    let role = 'admin';
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
      new_channel=$('#channel_template').clone().appendTo('#channel_menu');
      new_channel.prop('id', 'channel_'+channels.channels[0].name);
      new_channel.removeClass('d-none');
      new_channel_link = new_channel.children();
      new_channel_link.click({name: channels.channels[0].name}, getChannel);
      new_channel_label = new_channel.children().children()[1];
      new_channel_label.textContent = channels.channels[0].name;
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
  })
}

function getChannel(name) {
  alert(name.data.name);
}