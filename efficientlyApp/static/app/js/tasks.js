document.addEventListener("DOMContentLoaded", () => {
    // Textarea auto-expansion logic
    const expandTextarea = (textarea) => {
        if (textarea) {
            textarea.style.height = "auto";
            textarea.style.height = `${textarea.scrollHeight}px`;
        }
    };

    document.querySelectorAll("textarea").forEach((textarea) => {
        expandTextarea(textarea); // Initial expansion
        textarea.addEventListener("input", function () {
            expandTextarea(this); // Expansion on input
        });
    });

    // Tags Management
    const tagsContainer = document.getElementById("tags-container");
    const newTagInput = document.getElementById("new-tag");
    const tagsInput = document.getElementById("tags-input");
    const addTagButton = document.getElementById("add-tag");
    const updateTagsValue = () => {
        const remainingTags = Array.from(tagsContainer.querySelectorAll(".tag"))
            .map(tag => tag.textContent.trim().replace("x", "").trim());
        tagsInput.value = remainingTags.join(",");
    };
    addTagButton.addEventListener("click", () => {
        const tagValue = newTagInput.value.trim();
        if (tagValue) {
            const existingTags = tagsInput.value ? tagsInput.value.split(",") : [];
            if (!existingTags.includes(tagValue)) {
                existingTags.push(tagValue);
                tagsInput.value = existingTags.join(",");
                tagsContainer.insertAdjacentHTML(
                    "beforeend",
                    `<span class="tag bg-green-600 text-white px-2 py-1 rounded flex items-center gap-2">
                        ${tagValue}
                        <button type="button" class="remove-tag text-white bg-red-500 px-1 rounded">x</button>
                    </span>`
                );
                newTagInput.value = "";
            }
        }
    });
    tagsContainer.addEventListener("click", (e) => {
        if (e.target.classList.contains("remove-tag")) {
            const tagElement = e.target.parentElement;
            tagElement.remove();
            updateTagsValue();
        }
    });

    // Steps Management with auto-expanding textareas
    const stepsContainer = document.getElementById("steps-container");
    const addStepButton = document.getElementById("add-step");

    new Sortable(stepsContainer, {
        animation: 200, 
        swapThreshold: 0.65, 
        ghostClass: 'sortable-ghost', 
        chosenClass: 'sortable-chosen', 
        dragClass: 'sortable-drag',
    });

    addStepButton.addEventListener("click", () => {
        const stepTemplate = `
            <div class="step flex items-center gap-4" draggable="true">
                <label class="custom-checkbox">
                    <input type="hidden" name="step_complete[]" value="0">
                    <input type="checkbox" name="step_complete[]" value="1">
                    <span class="checkbox-mark"></span>
                </label>
                <textarea type="text" name="step_name[]" placeholder="Step name" class="input-like step-name" rows = 1></textarea>
                <input type="date" name="step_due_date[]" class="input-like w-40">
                <span class="remove-btn text-red-500 font-bold cursor-pointer">Remove</span>
            </div>`;
        stepsContainer.insertAdjacentHTML("beforeend", stepTemplate);

        // Apply auto-expansion logic to newly added textareas
        const newStepTextareaList = stepsContainer.querySelectorAll(".step-name");
        const newStepTextarea = newStepTextareaList[newStepTextareaList.length-1];
        console.log(newStepTextarea);
        if (newStepTextarea) {
            expandTextarea(newStepTextarea);
            newStepTextarea.addEventListener("input", function () {
                expandTextarea(this);
            });
        }
    });

    stepsContainer.addEventListener("click", (e) => {
        if (e.target.classList.contains("remove-btn")) {
            e.target.parentElement.remove();
        } else if (e.target.type === "checkbox") {
            const step = e.target.closest(".step");
            step.classList.toggle("completed");
        }
    });
});