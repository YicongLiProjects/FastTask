fnField = document.getElementById("firstNameField");
lnField = document.getElementById("lastNameField");
dobField = document.getElementById("dobField");
emailField = document.getElementById("emailField");
usernameField = document.getElementById("usernameField");
passwordField = document.getElementById("passwordField");
signupButton = document.getElementById("signupButton");
signupMessageDisplay = document.getElementById("signupMessageDisplay");

signupButton.addEventListener("click", async () => {
    const signup_data = {
        first_name: fnField.value,
        last_name: lnField.value,
        dob: dobField.value,
        email: emailField.value,
        display_name: usernameField.value,
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
        const signup_response = await fetch(request);
        const data = await signup_response.json();
        if (!signup_response.ok) {
            signupMessageDisplay.textContent = data.error;
            signupMessageDisplay.style.display = "block";
        }
        else {
            signupMessageDisplay.style.color = "#333333";
            signupMessageDisplay.textContent = "Account created successfully! Please log in.";
            signupMessageDisplay.style.display = "block";
        }
    } catch (error) {
        console.error("Error occurred while signing up: ", error);
    }
});
