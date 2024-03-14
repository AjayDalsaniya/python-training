const pwField = document.querySelectorAll('.loginPassword'),
      pwShowHide = document.querySelectorAll('.showHidePw');


pwShowHide.forEach(eyeIcon => {
        eyeIcon.addEventListener("click", ()=>{
            pwField.forEach(pawField => {
                if(pawField.type === "password"){
                    pawField.type = "text";
    
                    pwShowHide.forEach(icon => {
                        icon.classList.replace("uil-eye-slash","uil-eye");
                    })
    
                }else{
                    pawField.type = "password";
    
                    pwShowHide.forEach(icon => {
                        icon.classList.replace("uil-eye","uil-eye-slash");
                    })
                }
            })
        })
})

function closeLoginForm(){
    location.replace("http://127.0.0.1:5500/html/home.html");
}