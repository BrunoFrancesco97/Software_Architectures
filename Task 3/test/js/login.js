function login(){
    username =document.getElementsByClassName('text_login')[0].value;
    password = document.getElementsByClassName('password_login')[0].value;
    console.log(username + " "+ password);
    let encodedString = btoa(username+":"+password);
    console.log(encodedString);
    performLogin(encodedString);
    
}

function performLogin(hash){
    var request = new XMLHttpRequest();
    request.open("GET", "http://localhost:5000/login", true);
    request.onreadystatechange = function() {
        if(this.status == 200){
            window.location.replace("home.html");   
        }else{
            //TODO: MOSTRARE ERRORE CREDENZIALI
        }
    };
    request.withCredentials = true;
    request.setRequestHeader("Authorization", "Basic "+hash);
    request.send();
}