let pfpUploadBtn = document.getElementById('pfpUploadBtn');
let pfpFileInput = document.getElementById('pfpFileInput');

pfpUploadBtn.onclick = function() {
    pfpFileInput.style.display = 'block';
    pfpFileInput.click();
    pfpFileInput.style.display = 'none';
}