let signupBtn = document.getElementById("signupBtn");
let signinBtn = document.getElementById("signinBtn");
let nameField = document.getElementById("name");
let formTitle = document.getElementById("formTitle");

signinBtn.onclick = () => {
    nameField.style.maxHeight = "0";
    formTitle.innerHTML = "Sign In"
    signupBtn.classList.add("disable")
    signinBtn.classList.remove("disable")
}

signupBtn.onclick = () => {
    nameField.style.maxHeight = "65px";
    formTitle.innerHTML = "Sign Up"
    signupBtn.classList.remove("disable")
    signinBtn.classList.add("disable")
}