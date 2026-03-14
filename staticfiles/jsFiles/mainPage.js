signUpButton = document.getElementById("signUpButton");
loginButton = document.getElementById("loginButton");
helpButton = document.getElementById("helpButton");

signUpButton.onclick = function() {
    window.location.href = '/signup/';
};

loginButton.onclick = function() {
    window.location.href = '/login/';
};

helpButton.onclick = function() {
    window.location.href = '/help/';
};