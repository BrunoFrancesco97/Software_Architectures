function register(){
    let username =document.getElementsByClassName('text_login')[0].value;
    let password = document.getElementsByClassName('password_login')[0].value;
    let name = document.getElementsByClassName('text_name')[0].value;
    let surname = document.getElementsByClassName('text_surname')[0].value;
    let roleDiv = document.getElementsByClassName('content_role');
    let role = roleDiv[0].options[roleDiv[0].selectedIndex].value;
    if(username != null && password != null && name != null && surname != null && role != null){
        username.replaceAll(' ', '');
        password.replaceAll(' ', '');
        name.replaceAll(' ', '');
        surname.replaceAll(' ', '');
        role.replaceAll(' ', '');
        if(username != "" && password != "" && name != "" && surname != "" && role != ""){
            var request = new XMLHttpRequest();
            request.open("POST", "http://localhost:5000/login", true);
            request.setRequestHeader('Content-Type', 'application/json');
            request.onreadystatechange = function() {
                if(this.status == 200){
                    window.location.replace("home.html");   
                }else{
                    document.getElementById('wrong_credentials').style.display = 'inline';
                }
            };
            //request.withCredentials = true;
            request.send(JSON.stringify({"email":username,"password":password,"name":name,"surname":surname,"role":role}));
        } 
    }
}