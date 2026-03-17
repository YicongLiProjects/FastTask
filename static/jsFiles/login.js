emailField = document.getElementById("emailField");
passwordField = document.getElementById("passwordField");
signInButton = document.getElementById("signInButton");
loginErrorDisplay = document.getElementById("loginErrorDisplay");

signInButton.addEventListener("click", async () => {
    const login_data = {
        email: emailField.value,
        password: passwordField.value
    };
    const request = new Request("/login/submit/", {
        method: "POST",
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify(login_data)
    });
    try {
        const response = await fetch(request);
        if (!response.ok) {
            loginErrorDisplay.style.display = "block";
            loginErrorDisplay.textContent = response.error;
        }
        else {
            window.location.href='/app/';
        }
    } catch (error) {
        console.error("Error occurred while logging in:", error);
    }
})