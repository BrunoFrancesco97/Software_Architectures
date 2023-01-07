BASE_URL='http://localhost:5000/';

ENDPOINT_LOGIN='login';
ENDPOINT_LOGOUT='logout';
ENDPOINT_USER='user';

//login
function login(){
    if(is_form_valid()){
			$('#login_loading').removeClass('d-none');
      email=$('#email').val().replaceAll(' ', '');
      password=$('#password').val().replaceAll(' ', '');
      let encodedString = btoa(email+":"+password);
      api_login(encodedString);
    }
  }

function logged_in(){
logged=true;
display('home');
$('#invalid_credentials').addClass('d-none');
$('#login_loading').addClass('d-none');
}

function api_login(hash){
var request = new XMLHttpRequest();
var requestU = new XMLHttpRequest();
request.open("GET", BASE_URL+ENDPOINT_LOGIN, true);
request.onreadystatechange = function() {
  if(this.status == 200 && request.readyState == 4){
    //obj = JSON.parse(request);
    console.log('login ok');
    
    requestU.open("GET", BASE_URL+ENDPOINT_USER, true);
    requestU.onreadystatechange = function() {
      console.log('user');
      if(requestU.status == 200){
        console.log('user ok');
        obj = JSON.parse(request.responseText);
        console.log(obj);
        logged_in();
      } else {
      console.log('fail user');
      display('login');
      }
    }
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
console.log("sent!");
}

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
}