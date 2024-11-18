document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById("task-search");
    const tagFilter = document.getElementById("tag-filter");
    const taskContainer = document.getElementById('task-container');
    const tasks = Array.from(taskContainer.getElementsByClassName('task'));

    // Populate tag filter dropdown
    const uniqueTags = new Set();
    tasks.forEach(task => {
        const tags = task.dataset.tags.split(',');
        tags.forEach(tag => uniqueTags.add(tag.trim()));
    });
    uniqueTags.forEach(tag => {
        const option = document.createElement('option');
        option.value = tag;
        option.textContent = tag;
        tagFilter.appendChild(option);
    });

    // Filter tasks by name and tag
    const filterTasks = () => {
        const query = searchInput.value;
        const selectedTag = tagFilter.value;
        taskContainer.innerHTML = '';

        tasks
            .filter(task => {
                const matchesName = task.dataset.name.startsWith(query);
                const matchesTag = !selectedTag || task.dataset.tags.split(',').map(tag => tag.trim()).includes(selectedTag);
                return matchesName && matchesTag;
            })
            .forEach(task => taskContainer.appendChild(task));
    };

    // Attach event listeners
    searchInput.addEventListener('input', filterTasks);
    tagFilter.addEventListener('change', filterTasks);
});
