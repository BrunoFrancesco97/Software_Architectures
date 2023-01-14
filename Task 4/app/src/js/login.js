function login(){
    username =document.getElementsByClassName('text_login')[0].value;
    password = document.getElementsByClassName('password_login')[0].value;
    if(username != null && password != null){
        username.replaceAll(' ', '');
        password.replaceAll(' ', '');
        if(username != "" && password != ""){
            let encodedString = btoa(username+":"+password);
            performLogin(encodedString);
        } 
    }
}

function performLogin(hash){
    var request = new XMLHttpRequest();
    request.open("GET", "http://localhost:5000/login", true);
    request.onreadystatechange = function() {
        if(this.status == 200){
            window.location.replace("home.html");   
        }else{
            document.getElementById('wrong_credentials').style.display = 'inline';
            //TODO: MOSTRARE ERRORE CREDENZIALI
        }
    };
    request.withCredentials = true;
    request.setRequestHeader("Authorization", "Basic "+hash);
    request.send();
}

function staff(){
    window.location.replace("http://localhost:8080/staff/");
}