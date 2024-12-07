document.addEventListener("DOMContentLoaded", () => {
    const tasks = [
        "Start your journey",
        "Use Efficiently for efficiency",
        "Achieve your dreams"
    ];
    const taskContainer = document.getElementById("task-animation");
    let index = 0;

    function typeAndDeleteTask(task, container, callback) {
        let charIndex = 0;
        let isTyping = true;

        function type() {
            if (charIndex < task.length) {
                container.textContent += task[charIndex];
                charIndex++;
                setTimeout(type, 100); // Typing speed
            } else {
                isTyping = false;
                setTimeout(deleteText, 1000); // Delay before deleting
            }
        }

        function deleteText() {
            if (charIndex > 0) {
                container.textContent = task.substring(0, charIndex - 1);
                charIndex--;
                setTimeout(deleteText, 50); // Backspacing speed
            } else {
                isTyping = true;
                callback();
            }
        }

        if (isTyping) {
            type();
        }
    }

    function displayTasks() {
        if (index >= tasks.length) {
            index = 0; // Reset for looping
        }

        const taskElement = document.createElement("div");
        taskElement.className = "task";
        taskContainer.innerHTML = ""; // Clear previous task
        taskContainer.appendChild(taskElement);

        typeAndDeleteTask(tasks[index], taskElement, () => {
            index++;
            setTimeout(displayTasks, 500); // Delay before next task
        });
    }

    displayTasks();
});