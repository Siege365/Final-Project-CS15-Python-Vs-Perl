/**
 * Common Utilities
 * Shared functions for kebab menus across admin pages
 */

/**
 * Initialize kebab menu dropdowns
 */
function initKebabMenus() {
    // Kebab menu functionality
    document.querySelectorAll('.kebab-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            // Close all other open menus
            document.querySelectorAll('.kebab-menu.open').forEach(menu => {
                if (menu !== this.parentElement) {
                    menu.classList.remove('open');
                }
            });
            // Toggle current menu
            this.parentElement.classList.toggle('open');
        });
    });

    // Close kebab menus when clicking outside
    document.addEventListener('click', function() {
        document.querySelectorAll('.kebab-menu.open').forEach(menu => {
            menu.classList.remove('open');
        });
    });

    // Prevent dropdown clicks from closing the menu
    document.querySelectorAll('.kebab-dropdown').forEach(dropdown => {
        dropdown.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    });
}
