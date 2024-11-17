document.addEventListener('DOMContentLoaded', function () {
    const addTagBtn = document.getElementById('add-tag-btn');
    const tagsList = document.getElementById('tags-list');
    const addStepBtn = document.getElementById('add-step-btn');
    const stepsList = document.getElementById('steps-list');
    let tagCount = 0;
    let stepCount = 0;

    // Add Tag
    function addTagToForm(tagData = '') {
        const tagDiv = document.createElement('div');
        tagDiv.className = 'tag-item';
        tagDiv.innerHTML = `
            <input type="text" name="tags[]" value="${tagData}" placeholder="Tag Name" required />
            <span class="remove-tag-btn">Remove Tag</span>
        `;
        tagsList.appendChild(tagDiv);

        // Remove Tag
        tagDiv.querySelector('.remove-tag-btn').addEventListener('click', function () {
            tagsList.removeChild(tagDiv);
        });

        tagCount++;
    }

    addTagBtn.addEventListener('click', function () {
        addTagToForm();
    });

    // Add Step
    function addStepToForm(stepData = {}) {
        const stepDiv = document.createElement('div');
        stepDiv.className = 'step-item';
        stepDiv.innerHTML = `
            <div class="form-group">
                <label>Step Name:</label>
                <input type="text" name="step-${stepCount}-name" value="${stepData.name || ''}" placeholder="Step Name" required />
            </div>
            <div class="form-group">
                <label>Description:</label>
                <input type="text" name="step-${stepCount}-description" value="${stepData.description || ''}" placeholder="Description" />
            </div>
            <div class="form-group">
                <label>Due Date:</label>
                <input type="date" name="step-${stepCount}-due_date" value="${stepData.due_date || ''}" />
            </div>
            <span class="remove-step-btn">Remove Step</span>
        `;
        stepsList.appendChild(stepDiv);

        // Remove Step
        stepDiv.querySelector('.remove-step-btn').addEventListener('click', function () {
            stepsList.removeChild(stepDiv);
        });

        stepCount++;
    }

    addStepBtn.addEventListener('click', function () {
        addStepToForm();
    });
});
