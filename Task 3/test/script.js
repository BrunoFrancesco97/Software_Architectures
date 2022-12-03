
function get_courses(name){
    var request = new XMLHttpRequest();
    request.open("GET", "http://localhost:5000/channel/"+name, true);
    request.onreadystatechange = function() {
    if(request.status == 200 && request.readyState == 4){
        obj = JSON.parse(request.responseText);
        console.log(obj);
        for(let i = 0; i < obj.length; i++){
            console.log(obj[i])
            parent_div = document.querySelector('#course_template');
            //Remove all previous loaded channels 
            element_to_delete = document.querySelector('#course_template :not(.course_template)');
            for (let i = 0; i < parent_div.length; i++) {
                parent_div[i].parentNode.removeChild(els[i])
            }
            //Clone div so to add new courses 
            let clone = parent_div.cloneNode( true );  
            clone.classList.remove('course_template') //remove course_template thus this new cloned div is ok and no more a template to copy
            let name = document.getElementsByClassName('name');
            let id = document.getElementsByClassName('id');    
            clone.setAttribute( 'id', obj.channels[i].channel );
            name[0].innerText = obj.channels[i].name
            id[0].innerText = obj.channels[i].channel
            document.querySelector('#course_template').appendChild( clone ); 
        }
    }
    };
    request.withCredentials = true;
    request.send();
}

function get_materials(){
    
}


