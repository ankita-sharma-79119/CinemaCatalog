function disable_button(){
    var btn = document.getElementById("previous");
    if(btn.value == 0){
        document.getElementById("previous").disabled = true;
        document.getElementById("previous_link").style.pointerEvents = "none";
    }else{
        document.getElementById("previous").disabled = false;
    }
    
    let page_num = document.getElementById("btn_3").innerText;
    console.log(page_num);
    if(count == 500){
        document.getElementById("next").disabled = true;
        document.getElementById("next_link").style.pointerEvents = "none";
    }
}
window.onload = disable_button()