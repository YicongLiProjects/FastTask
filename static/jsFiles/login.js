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
        body: JSON.stringify(login_data),
        credentials: 'include'
    });
    try {
        const response = await fetch(request);
        const data = await response.json();
        if (!response.ok) {
            loginErrorDisplay.textContent = data.error;
            loginErrorDisplay.style.display = "block";
        }
        else {
            const urlParams = new URLSearchParams(window.location.search);
            const nextUrl = urlParams.get('next') || '/app/';
            window.location.href= nextUrl;
        }
    } catch (error) {
        console.error("Error occurred while logging in:", error);
    }
})