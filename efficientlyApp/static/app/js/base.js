document.addEventListener('DOMContentLoaded', () => {
    const menu = document.getElementById('menu');
    const menuBtn = document.getElementById('menu-btn');
    menuBtn.addEventListener('click', () => {
        menu.classList.toggle('hidden');
    });

    const profileDropdown = document.getElementById('profile-dropdown');
    const profileBtn = document.getElementById('profile-dropdown-btn');
    profileBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        profileDropdown.classList.toggle('hidden');
    });

    document.addEventListener('click', (e) => {
        if (!profileDropdown.contains(e.target) && !profileBtn.contains(e.target)) {
            profileDropdown.classList.add('hidden');
        }
    });
});