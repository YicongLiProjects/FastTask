let pfpUploadBtn = document.getElementById('pfpUploadBtn');
let pfpFileInput = document.getElementById('pfpFileInput');
let submitChangesBtn = document.getElementById('submitChangesBtn');
let cancelChangesBtn = document.getElementById('cancelChangesBtn');

let fnField = document.getElementById('fnField');
let lnField = document.getElementById('lnField');
let dobField = document.getElementById('dobField');
let emailField = document.getElementById('emailField');
let usernameField = document.getElementById('usernameField');
let passwordField = document.getElementById('passwordField');

let pfpImage = document.getElementById('pfpImage');

let statusMsgSection = document.getElementById('statusMsgSection');

pfpUploadBtn.onclick = function() {
    pfpFileInput.style.display = 'block';
    pfpFileInput.click();
    pfpFileInput.style.display = 'none';
}

pfpFileInput.onchange = function() {
    const file = this.files[0];
    if (file) {
        pfpImage.src = URL.createObjectURL(file);
    }
}

cancelChangesBtn.addEventListener('click', function() {
    clear();
});

submitChangesBtn.addEventListener('click', async () => {
    const formData = new FormData();
    formData.append('first_name', fnField.value);
    formData.append('last_name', lnField.value);
    formData.append('dob', dobField.value);
    formData.append('email', emailField.value);
    formData.append('display_name', usernameField.value);
    formData.append('password', passwordField.value);
    if (pfpFileInput.files.length > 0) {
        formData.append('pfp', pfpFileInput.files[0]);
    }
    // Request must contain the backend method to call, method, header, credentials and body
    const request = new Request("/update_profile/", {
        method: "POST",
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        credentials: 'include',
        body: formData
    });
    try {
        const response = await fetch(request);
        const data = await response.json();
        if (response.ok) {
            statusMsgSection.textContent = "Profile info updated successfully! Please save your password, email and username if applicable.";
            statusMsgSection.style.display = "block";
            // This executes after 2 seconds, clearing the status message
            setTimeout(() => {
                statusMsgSection.textContent = '';
                statusMsgSection.style.display = 'none';
            }, 2000);
        }
        else {
            statusMsgSection.textContent = data.error;
            statusMsgSection.style.display = "block";
        }
    } catch (error) {
        console.error("Error occurred while updating profile: ", error);
    }
});

// Clear all fields when cancel button is clicked or when info is saved
function clear() {
    fnField.value = '';
    lnField.value = '';
    dobField.value = '';
    emailField.value = '';
    usernameField.value = '';
    passwordField.value = '';
    pfpImage.src = '';
    statusMsgSection.textContent = '';
    statusMsgSection.style.display = 'none';
}
