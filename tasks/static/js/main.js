document.getElementById('add-step-btn').addEventListener('click', function () {
    const stepsContainer = document.getElementById('steps-container');
    const stepIndex = stepsContainer.children.length; // Calculate the current step index

    const stepRow = document.createElement('div');
    stepRow.classList.add('step-row');
    stepRow.innerHTML = `
        <div>
            <label for="step-${stepIndex}-name">Step Name:</label>
            <input type="text" name="step-${stepIndex}-name" id="step-${stepIndex}-name" placeholder="Enter step name" required>
        </div>
        <div>
            <label for="step-${stepIndex}-description">Step Description:</label>
            <textarea name="step-${stepIndex}-description" id="step-${stepIndex}-description" placeholder="Enter step description" required></textarea>
        </div>
        <div>
            <label for="step-${stepIndex}-due_date">Step Due Date:</label>
            <input type="date" name="step-${stepIndex}-due_date" id="step-${stepIndex}-due_date" required>
        </div>
    `;

    stepsContainer.appendChild(stepRow);
});
