let addButton = document.getElementById("addButton");
let closeButton = document.getElementsByClassName("close_btn")[0];
let saveTaskButton = document.getElementById("saveTaskBtn");
let resetButton = document.getElementById("resetBtn");
let pfpButton = document.getElementById("pfpButton");
let deleteTaskButton = document.getElementById("deleteTaskBtn");
let helpButton = document.getElementById("helpBtn");
let accountDetailsButton = document.getElementById("accountDetailsBtn");
let logoutButton = document.getElementById("logoutBtn");
let completeButton = document.getElementById("taskCompletedBtn");

let modalBox = document.getElementById("taskModalBox");

let taskNameInput = document.getElementById("taskName");
let taskEnd = document.getElementById("taskEnd");
let remindAt = document.getElementById("remindAt");
let taskNotes = document.getElementById("taskNotes");
let accountBox = document.getElementById("accountBox");

let taskContainer = document.getElementById("taskContainer");
let modalTitle = document.getElementById("modalTitle");

let xpValue = document.getElementById("xpValue");
let levelValue = document.getElementById("levelValue");

let clickedElement = null;

// List containing all tasks 
let tasksRequest = new Request("/get_tasks/", {
    method: "GET",
    headers: {
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
    }
});

let tasks = [];

function formatDateTime(dateTimeStr) {
    if (!dateTimeStr || dateTimeStr.length < 16) {
        return '';
    }
    date = dateTimeStr.slice(0, 10);
    t = 'T';
    time = dateTimeStr.slice(11, 16);
    formattedDateTime = date + t + time;
    return formattedDateTime;
}
// Load tasks from the database and add them while styling it using a helper defined at the end.
// Do this and styling with Django's for loop with {{}} in the HTML file to make the task easier
async function loadTasks() {
    try {
        const response = await fetch(tasksRequest);
        tasks_json = await response.json();
        tasks = tasks_json.tasks;
        // Use the field names as in the model (database)!!!!!!!!!!
        tasks.forEach(t => addTask(t.title, formatDateTime(t.deadline), formatDateTime(t.remindAt), t.notes, t.taskID));
    } catch (e) {
        console.error("Error loading tasks: ", e);
    }
}

// Load tasks into the page, execute only when DOM fully loaded 
// When querying from database, always async / await to ensure everything loads properly
document.addEventListener("DOMContentLoaded", async () => {
    await loadTasks();
});

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

saveTaskButton.addEventListener("click", async () => {
    modalBox.style.display = "none";

    const taskData = {
        title: taskNameInput.value,
        deadline: taskEnd.value,
        remindAt: remindAt.value,
        notes: taskNotes.value,
    };
    if (modalTitle.innerText === "Add new task") {
        taskData.task_id = crypto.randomUUID();
        const request = new Request("/add_task/", {
        method: "POST", 
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify(taskData)
        });

        try {
            const response = await fetch(request);
            const data = await response.json();
            if (response.ok) {
                addTask(taskData.title, taskData.deadline, taskData.remindAt, taskData.notes, taskData.task_id);
            }
            else {
                alert("Error adding task: " + data.error);
            }
        } catch (error) {
            alert("Error adding task: " + error);
        }
    }
    else if (modalTitle.innerText === "Edit task") {
        taskData.task_id = clickedElement.id;
        const request = new Request("/edit_task/", {
        method: "POST", 
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify(taskData)
        });

        try {
            const response = await fetch(request);
            const data = await response.json();
            if (response.ok) {
                styleTask(clickedElement, taskData.task_id, taskData.title, taskData.deadline);
                // We can assume that the task ID does not change as we edit the task
                const i = tasks.findIndex(t => t.task_id === clickedElement.id);
                tasks[i] = taskData;
            }
            else {
                alert("Error editing task: " + data.error);
            }
        } catch (error) {
            alert("Error editing task: " + error);
        }
    }
});

resetButton.onclick = function() {
    clear();
}

taskContainer.addEventListener('click', function(e) {
    clickedElement = e.target.closest('button');
    if (clickedElement && taskContainer.contains(clickedElement)) {
        modalBox.style.display = "block";
        // Get task of this button
        const ID = clickedElement.id;
        const task = tasks.find(t => t.task_id === ID);

        // Populate modal with task info and restyle the modal box
        taskNameInput.value = task.title;
        taskEnd.value = formatDateTime(task.deadline);
        remindAt.value = formatDateTime(task.remindAt);
        taskNotes.value = task.notes;
        modalTitle.innerText = "Edit task";
        deleteTaskButton.disabled = false;
        completeButton.disabled = false;
    }
});

deleteTaskButton.addEventListener("click", async () => {
    if (clickedElement) {
        const taskID = clickedElement.id;
        const request = new Request("/remove_task/", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({task_id: taskID})
        });
        try {
            const response = await fetch(request);
            if (response.ok) {
                removeTask(clickedElement, taskID);
            }
        } catch (error) {
            alert("Error deleting task: " + error);
        }
    }
});

completeButton.addEventListener("click", async () => {
    if (clickedElement) {
        const taskID = clickedElement.id;
        const request = new Request("/complete_task/", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({task_id: taskID})
        });
        try {
            const response = await fetch(request);
            if (response.ok) {
                removeTask(clickedElement, taskID);

                // Update XP and level on the client end to reflect changes on the server end
                xpValue.textContent = parseInt(xpValue.textContent.split(" ")[0]) + 20 + " XP";
                if (parseInt(xpValue.textContent) >= 100 * parseInt(levelValue.textContent.split(" ")[1])) {
                    levelValue.textContent = "Level " + (parseInt(levelValue.textContent.split(" ")[1]) + 1);
                    xpValue.textContent = 0 + " XP";
                }
            }
        } catch (error) {
            alert("Error marking task as completed: " + error);
        }
    }
});

helpButton.onclick = function() {
    document.location.href = "/help/";
}

accountDetailsButton.onclick = function() {
    document.location.href = "/account_info/";
}

logoutButton.addEventListener("click", async () => {
    const request = new Request("/logout/submit/", {
        method: "POST",
        headers: {
            "Content-Type": 'application/json',
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    });
    try {
        const response = await fetch(request);
        if (response.ok) {
            document.location.href = "/login/";
        }
    } catch (error) {
        alert("Error logging out: " + error);
    }
});

// Style the task button
function styleTask(taskBtn, id, title, deadline) {
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
    taskBtn.id = id;
    taskBtn.innerHTML = title + "<br>Due on: " + new Date(deadline).toLocaleDateString() + " " + new Date(deadline).toLocaleTimeString();
}

// Create one HTML button for each task from data, client end
function addTask(taskName, taskDue, taskRemind, notesOfTask, taskId) {
    const newTaskBtn = document.createElement("button");
    
    let task = {
        title: taskName,
        deadline: taskDue,
        remindAt: taskRemind,
        notes: notesOfTask,
        task_id: taskId
    };

    styleTask(newTaskBtn, taskId, taskName, taskDue);
    tasks.push(task);
    taskContainer.appendChild(newTaskBtn);
}

function removeTask(clicked, taskID) {
    tasks = tasks.filter(t => t.task_id !== taskID);
    taskContainer.removeChild(clicked);
    modalBox.style.display = "none";
    clickedElement = null;
    deleteTaskButton.disabled = true;
} 

function clear() {
    document.getElementById("taskName").value = "";
    document.getElementById("taskEnd").value = "";
    document.getElementById("remindAt").value = "";
    document.getElementById("taskNotes").value = "";
}