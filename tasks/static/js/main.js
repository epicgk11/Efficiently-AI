document.addEventListener('DOMContentLoaded', function () {
    const taskBoxes = document.querySelectorAll('.task-box');
    const popupOverlay = document.getElementById('popup-overlay');
    const closePopupBtn = document.getElementById('close-popup');
    const editTaskForm = document.getElementById('edit-task-form');
    const stepsContainer = document.getElementById('steps-container');
    const addStepBtn = document.getElementById('add-step-btn');
    const tagsList = document.getElementById('tags-list');
    const addTagBtn = document.getElementById('add-tag-btn');

    let stepCount = 0;
    let tagCount = 0;

    // Function to fetch CSRF token from cookies
    function getCSRFToken() {
        const name = 'csrftoken=';
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name)) {
                return cookie.substring(name.length, cookie.length);
            }
        }
        return null;
    }

    // Function to open the edit popup and populate it with task data
    function openEditPopup(taskId) {
        fetch(`/tasks/get/${taskId}/`)
            .then(response => response.json())
            .then(data => {
                populateEditForm(data.task['task']);
                popupOverlay.style.display = 'flex';
            })
            .catch(error => console.error('Error fetching task data:', error));
    }

    // Attach click event to task boxes
    taskBoxes.forEach(box => {
        box.addEventListener('click', function () {
            const taskId = this.getAttribute('data-task-id');
            openEditPopup(taskId);
        });
    });

    // Close the popup
    closePopupBtn.addEventListener('click', function () {
        popupOverlay.style.display = 'none';
        editTaskForm.reset();
        stepsContainer.innerHTML = '<h3>Steps</h3>';
        tagsList.innerHTML = '';
        stepCount = 0;
        tagCount = 0;
    });

    // Populate the edit form with task data
    function populateEditForm(task) {
        document.getElementById('task-id').value = task.id || task._id;
        document.getElementById('task-name').value = task.name || '';
        document.getElementById('task-description').value = task.description || '';
        document.getElementById('task-due-date').value = task.due_date || '';
        document.getElementById('task-resources').value = task.resources || '';
        document.getElementById('task-completed').checked = task.completed || false;

        // Populate tags
        tagsList.innerHTML = '';
        tagCount = 0;
        if (task.tags) {
            task.tags.forEach(tag => addTagToForm(tag));
        }

        // Populate steps
        stepsContainer.innerHTML = '<h3>Steps</h3>';
        stepCount = 0;
        if (task.steps) {
            task.steps.forEach(step => addStepToForm(step));
        }
    }

    // Add a tag input to the form
    function addTagToForm(tagName = '') {
        const tagDiv = document.createElement('div');
        tagDiv.className = 'tag-item';
        tagDiv.innerHTML = `
            <input type="text" name="tag-${tagCount}-name" value="${tagName}" placeholder="Tag Name" required />
            <span class="remove-tag-btn">Remove Tag</span>
        `;
        tagsList.appendChild(tagDiv);
        tagDiv.querySelector('.remove-tag-btn').addEventListener('click', function () {
            tagsList.removeChild(tagDiv);
        });
        tagCount++;
    }

    // Add a new tag on button click
    addTagBtn.addEventListener('click', function () {
        addTagToForm();
    });

    // Add a step input to the form
    function addStepToForm(step = {}) {
        const stepDiv = document.createElement('div');
        stepDiv.className = 'step-item';
        stepDiv.innerHTML = `
            <div class="form-group">
                <label>Step Name:</label>
                <input type="text" name="step-${stepCount}-name" value="${step.name || ''}" required />
            </div>
            <div class="form-group">
                <label>Description:</label>
                <input type="text" name="step-${stepCount}-description" value="${step.description || ''}" />
            </div>
            <div class="form-group">
                <label>Due Date:</label>
                <input type="date" name="step-${stepCount}-due_date" value="${step.due_date || ''}" />
            </div>
            <div class="form-group">
                <label>Completed:</label>
                <input type="checkbox" name="step-${stepCount}-completed" ${step.completed ? 'checked' : ''} />
            </div>
            <span class="remove-step-btn">Remove Step</span>
            <hr>
        `;
        stepsContainer.appendChild(stepDiv);
        stepDiv.querySelector('.remove-step-btn').addEventListener('click', function () {
            stepsContainer.removeChild(stepDiv);
        });
        stepCount++;
    }

    // Add a new step on button click
    addStepBtn.addEventListener('click', function () {
        addStepToForm();
    });

    // Handle form submission
    editTaskForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const formData = new FormData(editTaskForm);
        const taskId = formData.get('task_id');
        const data = { steps: [], tags: [] };

        formData.forEach((value, key) => {
            if (key === 'task_id') {
                // Exclude task_id from data
            } else if (key.startsWith('step-')) {
                const [, index, field] = key.split('-');
                data.steps[index] = data.steps[index] || {};
                data.steps[index][field] = value;
            } else if (key.startsWith('tag-')) {
                const [, index] = key.split('-');
                data.tags[index] = value;
            } else {
                data[key] = value;
            }
        });

        data.steps = data.steps ? Object.values(data.steps) : [];
        data.tags = data.tags ? Object.values(data.tags) : [];
        data.completed = formData.get('completed') === 'on';

        fetch(`/tasks/update/${taskId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify(data),
        })
            .then(response => {
                if (response.ok) {
                    location.reload();
                } else {
                    alert('Failed to update task.');
                }
            })
            .catch(error => console.error('Error updating task:', error));
    });
});