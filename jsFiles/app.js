let addButton = document.getElementById("addButton");
let modalBox = document.getElementById("taskModalBox");
let closeButton = document.getElementsByClassName("close_btn")[0];
let saveTaskButton = document.getElementById("saveTaskBtn");

addButton.onclick = function() {
    modalBox.style.display = "block";
}

closeButton.onclick = function() {
    modalBox.style.display = "none";
}

window.onclick = function(event) {
    if (event.target == modalBox) {
        modalBox.style.display = "none";
    }
}

saveTaskButton.onclick = function() {
    modalBox.style.display = "none";
    const newTask = document.createNewElement("button");
    newTask.style.width = "300px";
    newTask.style.height = "180px";
    document.body.appendChild(newTask);
}