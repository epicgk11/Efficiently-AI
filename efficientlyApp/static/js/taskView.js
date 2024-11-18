const tagsContainer = document.getElementById('tags-container');
const newTagInput = document.getElementById('new-tag');
const tagsInput = document.getElementById('tags-input');
const addTagButton = document.getElementById('add-tag');
const tags = tagsInput.value ? tagsInput.value.split(', ') : [];

addTagButton.addEventListener('click', () => {
    const tagValue = newTagInput.value.trim();
    if (tagValue && !tags.includes(tagValue)) {
        tags.push(tagValue);
        tagsInput.value = tags.join(', ');
        tagsContainer.insertAdjacentHTML('beforeend', `<span class="tag">${tagValue}</span>`);
        newTagInput.value = '';
    }
});

const stepsContainer = document.getElementById('steps-container');
const addStepButton = document.getElementById('add-step');

addStepButton.addEventListener('click', () => {
    const stepTemplate = `
        <div class="step">
            <input type="hidden" name="step_completed[]" value="0">
            <input type="checkbox" name="step_completed[]" value="1">
            <input type="text" name="step_name[]" class="input-like" placeholder="Step name">
            <input type="date" name="step_due_date[]" class="input-like">
            <span class="remove-btn text-red-500 font-bold cursor-pointer">Remove</span>
        </div>
    `;
    stepsContainer.insertAdjacentHTML('beforeend', stepTemplate);
});

stepsContainer.addEventListener('click', (e) => {
    if (e.target.classList.contains('remove-btn')) {
        e.target.parentElement.remove();
    }
});


