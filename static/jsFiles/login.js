emailField = document.getElementById("emailField");
passwordField = document.getElementById("passwordField");
signInButton = document.getElementById("signInButton");

signInButton.addEventListener("click", function() {
    submit();
})

function submit() {
    const login_data = {
        email: emailField.value,
        passwordField: passwordField.value
    };
    fetch("/login/", {
        method: "POST",
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify(login_data)
    }).then(response => response.json());
}