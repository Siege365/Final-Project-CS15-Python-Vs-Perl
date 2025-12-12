/**
 * Admin Product Edit
 * Update confirmation modal and form handling
 */

document.addEventListener('DOMContentLoaded', function() {
    // Update confirmation modal
    const form = document.getElementById('product-form');
    const modal = document.getElementById('update-modal');
    const modalClose = document.getElementById('modal-close');
    const cancelUpdate = document.getElementById('cancel-update');
    const confirmUpdate = document.getElementById('confirm-update');
    let formSubmitting = false;

    function closeModal() {
        modal.classList.remove('show');
    }

    modalClose.addEventListener('click', closeModal);
    cancelUpdate.addEventListener('click', closeModal);
    document.querySelector('#update-modal .modal-backdrop').addEventListener('click', closeModal);

    form.addEventListener('submit', function(e) {
        if (!formSubmitting) {
            e.preventDefault();
            modal.classList.add('show');
        }
    });

    confirmUpdate.addEventListener('click', function() {
        formSubmitting = true;
        const submitBtn = form.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-small"></span> Saving...';
        closeModal();
        form.submit();
    });

    // Category selection
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

    // Stock adjustment
    const adjustmentType = document.getElementById('adjustment_type');
    const adjustmentQtyGroup = document.getElementById('adjustment-quantity-group');
    const adjustmentReasonGroup = document.getElementById('adjustment-reason-group');

    if (adjustmentType) {
        adjustmentType.addEventListener('change', function() {
            if (this.value) {
                adjustmentQtyGroup.style.display = 'block';
                adjustmentReasonGroup.style.display = 'block';
            } else {
                adjustmentQtyGroup.style.display = 'none';
                adjustmentReasonGroup.style.display = 'none';
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

        // Remove image
        const removeImageBtn = document.getElementById('remove-image');
        if (removeImageBtn) {
            removeImageBtn.addEventListener('click', function() {
                imagePreview.style.display = 'none';
                uploadPlaceholder.style.display = 'flex';
                document.getElementById('image_url').value = '';
                document.getElementById('remove_image_flag').value = '1';
                this.style.display = 'none';
            });
        }

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
});
