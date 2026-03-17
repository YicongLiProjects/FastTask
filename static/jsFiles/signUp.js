fnField = document.getElementById("firstNameField");
lnField = document.getElementById("lastNameField");
dobField = document.getElementById("dobField");
emailField = document.getElementById("emailField");
usernameField = document.getElementById("usernameField");
passwordField = document.getElementById("passwordField");
signupButton = document.getElementById("signupButton");
signupErrorDisplay = document.getElementById("signupErrorDisplay");

signupButton.addEventListener("click", async () => {
    const signup_data = {
        fn: fnField.value,
        ln: lnField.value,
        date_of_birth: dobField.value,
        email: emailField.value,
        username: usernameField.value,
        password: passwordField.value
    };
    const request = new Request("/signup/submit/", {
        method: "POST",
        headers: {
            "Content-Type": 'application/json',
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify(signup_data)
    });
    try {
        const response = await fetch(request);
        if (!response.ok) {
            signupErrorDisplay.style.display = "block";
            signupErrorDisplay.textContent = response.error;
        }
        else {
            window.location.href='/app/';
        }
    } catch (error) {
        console.error("Error occurred while signing up:", error);
    }
});
