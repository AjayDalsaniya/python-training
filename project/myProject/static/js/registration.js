const spwField = document.querySelectorAll('.signupPassword'),
      pwShowHide1 = document.querySelectorAll('.showHidePw1');



pwShowHide1.forEach(eyeIcon1 => {
        eyeIcon1.addEventListener("click", ()=>{
            spwField.forEach(pawField1 => {
                if(pawField1.type === "password"){
                    pawField1.type = "text";
    
                    pwShowHide1.forEach(icon1 => {
                        icon1.classList.replace("uil-eye-slash","uil-eye");
                    })
                }else{
                    pawField1.type = "password";
    
                    pwShowHide1.forEach(icon1 => {
                        icon1.classList.replace("uil-eye","uil-eye-slash");
                    })
                }
            })
        })
    })

    function closeSignUpForm(){
        location.replace("http://127.0.0.1:5500/html/home.html")
    }