function logout(){
    var request = new XMLHttpRequest();
    request.open("GET", "http://localhost:5000/logout", true);
    request.onreadystatechange = function() {
        if(request.status == 200){
            window.location.replace("index.html");   
        }
    };
    request.withCredentials = true;
    request.send();
}