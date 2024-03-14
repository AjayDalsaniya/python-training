let loginForm = document.querySelector('.login-form');
let signupForm = document.querySelector('.signup-form');

const pwField = document.querySelectorAll('.loginPassword'),
      pwShowHide = document.querySelectorAll('.showHidePw'),
      spwField = document.querySelectorAll('.signupPassword'),
      pwShowHide1 = document.querySelectorAll('.showHidePw1');


// document.querySelector('#signin').onclick = () => {
//     loginForm.classList.add('active');
// }

// document.querySelector('#close-login-form').onclick = () => {
//     loginForm.classList.remove('active');
// }

// document.querySelector('#signin1').onclick = () => {
//     loginForm.classList.add('active');
//     signupForm.classList.remove('active');
// }

// document.querySelector('#signup').onclick = () => {
//     signupForm.classList.add('active');
//     loginForm.classList.remove('active');
// }

// document.querySelector('#close-signup-form').onclick = () => {
//     signupForm.classList.remove('active');
// }

let menu = document.querySelector('#menu-btn');
let navbar = document.querySelector('.header .nav');

menu.onclick = () => {
    menu.classList.toggle('fa-times');
    navbar.classList.toggle('active');
}

window.onscroll = () => {
    loginForm.classList.remove('active');
    menu.classList.remove('fa-times');
    navbar.classList.remove('active');

    if(window.scrollY > 0){
        document.querySelector('.header').classList.add('active');
    }else{
        document.querySelector('.header').classList.remove('active');
    }
}

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
