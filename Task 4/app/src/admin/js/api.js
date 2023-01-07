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
$('#login_loading').addClass('d-none');
}

function api_login(hash){
var request = new XMLHttpRequest();
request.open("GET", "http://localhost:5000/login", true);
request.onreadystatechange = function() {
    if(this.status == 200){
        logged_in();
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


function logout(){
var request = new XMLHttpRequest();
request.open("GET", "http://localhost:5000/logout", true);
request.onreadystatechange = function() {
if(request.status == 200){
    logged=false;
    display('login');
}
};
request.withCredentials = true;
request.send();
}