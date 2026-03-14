emailField = document.getElementById("emailField");
passwordField = document.getElementById("passwordField");
signInButton = document.getElementById("signInButton");
loginErrorDisplay = document.getElementById("loginErrorDisplay");

signInButton.addEventListener("click", async () => {
    const login_data = {
        email: emailField.value,
        passwordField: passwordField.value
    };
    const request = new Request("/login/", {
        method: "POST",
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify(login_data)
    });
    try {
        const response = await fetch(request);
        if (!response.ok) {
            loginErrorDisplay.textContent = response.statusText;
            loginErrorDisplay.style.display = "block";
        }
    } catch (error) {
        console.error("Error occurred while logging in:", error);
    }
})