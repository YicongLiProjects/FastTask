let addButton = document.getElementById("addButton");
let closeButton = document.getElementsByClassName("close_btn")[0];
let saveTaskButton = document.getElementById("saveTaskBtn");
let resetButton = document.getElementById("resetBtn");
let pfpButton = document.getElementById("pfpButton");
let deleteTaskButton = document.getElementById("deleteTaskBtn");
let helpButton = document.getElementById("helpBtn");
let accountDetailsButton = document.getElementById("accountDetailsBtn");
let logoutButton = document.getElementById("logoutBtn");

let modalBox = document.getElementById("taskModalBox");

let taskNameInput = document.getElementById("taskName");
let taskEnd = document.getElementById("taskEnd");
let remindAt = document.getElementById("remindAt");
let taskNotes = document.getElementById("taskNotes");
let accountBox = document.getElementById("accountBox");

let taskContainer = document.getElementById("taskContainer");
let modalTitle = document.getElementById("modalTitle");

let clickedElement = null;

let tasks = [];


pfpButton.onclick = function() {
    if (accountBox.style.display === "none") {
        accountBox.style.display = "block";
    }
    else {
        accountBox.style.display = "none";
    }
}

addButton.onclick = function() {
    clear();
    modalBox.style.display = "block";
    modalTitle.innerText = "Add new task";
    deleteTaskButton.disabled = true;
}

closeButton.onclick = function() {
    modalBox.style.display = "none";
}

window.onclick = function(event) {
    if (event.target == modalBox) {
        modalBox.style.display = "none";
    }
    if (event.target != pfpButton && event.target != accountBox) {
        accountBox.style.display = "none";
    }
}

saveTaskButton.onclick = function() {
    modalBox.style.display = "none";
    const newTask = document.createElement("button");
    
    const now = new Date();

    // Edge cases and input verification
    if (taskNameInput.value === "" || taskEnd.value === "") {
        alert("Please fill in all required fields.");
        return;
    }
    
    if (new Date(taskEnd.value) < now) {
        alert("The due date and time must be in the future.");
        return;
    }

    if (new Date(remindAt.value) < now || new Date(remindAt.value) > new Date(taskEnd.value)) {
        alert("The reminder time must be in the future and before the task's due time.");
        return;
    }

    const taskId = crypto.randomUUID();
    styleTask(newTask, taskId);

    let task = {
        taskID: taskId,
        name: taskNameInput.value,
        dueDate: taskEnd.value,
        remindAt: remindAt.value,
        notes: taskNotes.value
    };
    tasks.push(task);
    taskContainer.appendChild(newTask);
}

resetButton.onclick = function() {
    clear();
}

taskContainer.addEventListener('click', function(e) {
    clickedElement = e.target.closest('button');
    if (clickedElement && taskContainer.contains(clickedElement)) {
        modalBox.style.display = "block";
        // Retrieve task of this button
        const ID = clickedElement.style.id;
        const task = tasks.find(t => t.taskID === ID);

        // Populate modal with task info and restyle the modal box
        taskNameInput.value = task.name;
        taskEnd.value = task.dueDate;
        remindAt.value = task.remindAt;
        taskNotes.value = task.notes;
        modalTitle.innerText = "Edit task";
        deleteTaskButton.disabled = false;
    }
});

deleteTaskButton.onclick = function() {
    if (clickedElement) {
        const ID = clickedElement.style.id;
        tasks = tasks.filter(t => t.taskID !== ID);
        taskContainer.removeChild(clickedElement);
        modalBox.style.display = "none";
        clickedElement = null;
        deleteTaskButton.disabled = true;
    }
}

helpButton.onclick = function() {
    document.location.href = "helpPage.html";
}

accountDetailsButton.onclick = function() {
    document.location.href = "accountInfoPage.html";
}

logoutButton.onclick = function() {
    document.location.href = "loginPage.html";
}

// Helper functions
function styleTask(taskBtn, id) {
    taskBtn.style.width = "300px";
    taskBtn.style.height = "180px";
    taskBtn.style.borderRadius = "20px";
    taskBtn.style.marginTop = "20px";
    taskBtn.style.marginLeft = "10px";
    taskBtn.style.borderColor = "lightskyblue";
    taskBtn.style.backgroundColor = "white";
    taskBtn.style.color = "purple";
    taskBtn.style.fontSize = "20px";
    taskBtn.style.fontFamily = "Trebuchet MS, sans-serif";
    taskBtn.style.id = id;
    taskBtn.innerHTML = taskNameInput.value + "<br>Due on: " + new Date(taskEnd.value).toLocaleDateString() + " " + new Date(taskEnd.value).toLocaleTimeString();
}

function clear() {
    document.getElementById("taskName").value = "";
    document.getElementById("taskEnd").value = "";
    document.getElementById("remindAt").value = "";
    document.getElementById("taskNotes").value = "";
}