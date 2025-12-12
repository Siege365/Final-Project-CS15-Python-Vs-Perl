/**
 * Admin Product Add
 * Form handling with image upload preview
 */

document.addEventListener('DOMContentLoaded', function() {
    // Category selection - show new category field
    const categorySelect = document.getElementById('category');
    const newCategoryGroup = document.getElementById('new-category-group');
    const newCategoryInput = document.getElementById('new_category');

    if (categorySelect) {
        categorySelect.addEventListener('change', function() {
            if (this.value === '__new__') {
                newCategoryGroup.style.display = 'block';
                newCategoryInput.required = true;
            } else {
                newCategoryGroup.style.display = 'none';
                newCategoryInput.required = false;
            }
        });
    }

    // Image upload preview
    const imageInput = document.getElementById('image');
    const imagePreview = document.getElementById('image-preview');
    const uploadPlaceholder = document.getElementById('upload-placeholder');
    const uploadArea = document.getElementById('image-upload-area');

    if (uploadArea) {
        uploadArea.addEventListener('click', () => imageInput.click());

        imageInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    imagePreview.src = e.target.result;
                    imagePreview.style.display = 'block';
                    uploadPlaceholder.style.display = 'none';
                };
                reader.readAsDataURL(file);
            }
        });

        // Image URL preview
        const imageUrlInput = document.getElementById('image_url');
        if (imageUrlInput) {
            imageUrlInput.addEventListener('change', function() {
                if (this.value) {
                    imagePreview.src = this.value;
                    imagePreview.style.display = 'block';
                    uploadPlaceholder.style.display = 'none';
                }
            });
        }

        // Drag and drop
        uploadArea.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', function() {
            this.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', function(e) {
            e.preventDefault();
            this.classList.remove('dragover');
            
            const file = e.dataTransfer.files[0];
            if (file && file.type.startsWith('image/')) {
                imageInput.files = e.dataTransfer.files;
                const reader = new FileReader();
                reader.onload = function(e) {
                    imagePreview.src = e.target.result;
                    imagePreview.style.display = 'block';
                    uploadPlaceholder.style.display = 'none';
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // Form submission
    const form = document.getElementById('product-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner-small"></span> Adding...';
        });
    }
});
