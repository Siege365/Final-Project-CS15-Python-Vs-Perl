/**
 * Admin Products List
 * Handles product deletion and quick stock adjustment with kebab menu and modals
 */

document.addEventListener('DOMContentLoaded', function() {
    const deleteModal = document.getElementById('delete-modal');
    const modalClose = document.getElementById('modal-close');
    const cancelDelete = document.getElementById('cancel-delete');
    const confirmDelete = document.getElementById('confirm-delete');
    const productNameEl = document.getElementById('delete-product-name');
    let productToDelete = null;

    // Stock adjustment modal elements
    const stockModal = document.getElementById('stock-modal');
    const stockModalClose = document.getElementById('stock-modal-close');
    const cancelStock = document.getElementById('cancel-stock');
    const confirmStock = document.getElementById('confirm-stock');
    const stockProductNameEl = document.getElementById('stock-product-name');
    const currentStockDisplay = document.getElementById('current-stock-display');
    const adjustmentType = document.getElementById('adjustment-type');
    const adjustmentQuantity = document.getElementById('adjustment-quantity');
    const newStockPreview = document.getElementById('new-stock-preview');
    let productToAdjust = null;
    let currentStock = 0;

    if (!stockModal) return;

    // Initialize kebab menus
    initKebabMenus();

    // Open delete modal
    document.querySelectorAll('.delete-product-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            productToDelete = this.dataset.productId;
            productNameEl.textContent = this.dataset.productName;
            // Close kebab menu
            document.querySelectorAll('.kebab-menu.open').forEach(menu => {
                menu.classList.remove('open');
            });
            deleteModal.classList.add('show');
        });
    });

    // Open stock adjustment modal
    document.querySelectorAll('.quick-stock-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            productToAdjust = this.dataset.productId;
            currentStock = parseInt(this.dataset.currentStock);
            
            if (stockProductNameEl) stockProductNameEl.textContent = this.dataset.productName;
            if (currentStockDisplay) currentStockDisplay.textContent = currentStock;
            if (adjustmentQuantity) adjustmentQuantity.value = 0;
            
            updateStockPreview();
            
            // Close kebab menu
            document.querySelectorAll('.kebab-menu.open').forEach(menu => {
                menu.classList.remove('open');
            });
            
            stockModal.classList.add('show');
        });
    });

    // Update stock preview when values change
    function updateStockPreview() {
        if (!adjustmentType || !adjustmentQuantity || !newStockPreview) return;
        
        const type = adjustmentType.value;
        const quantity = parseInt(adjustmentQuantity.value) || 0;
        let newStock = currentStock;

        if (type === 'add') {
            newStock = currentStock + quantity;
        } else if (type === 'remove') {
            newStock = Math.max(0, currentStock - quantity);
        } else if (type === 'set') {
            newStock = quantity;
        }

        newStockPreview.textContent = `New Stock: ${newStock}`;
        newStockPreview.style.color = newStock === 0 ? 'var(--error)' : newStock <= 10 ? 'var(--warning)' : 'var(--success)';
    }

    if (adjustmentType) {
        adjustmentType.addEventListener('change', updateStockPreview);
    }
    
    if (adjustmentQuantity) {
        adjustmentQuantity.addEventListener('input', updateStockPreview);
    }

    // Close delete modal
    function closeDeleteModal() {
        deleteModal.classList.remove('show');
        productToDelete = null;
    }

    modalClose.addEventListener('click', closeDeleteModal);
    cancelDelete.addEventListener('click', closeDeleteModal);
    deleteModal.querySelector('.modal-backdrop').addEventListener('click', closeDeleteModal);

    // Close stock modal
    function closeStockModal() {
        stockModal.classList.remove('show');
        productToAdjust = null;
        currentStock = 0;
    }

    if (stockModalClose) {
        stockModalClose.addEventListener('click', closeStockModal);
    }
    
    if (cancelStock) {
        cancelStock.addEventListener('click', closeStockModal);
    }
    
    const stockBackdrop = stockModal ? stockModal.querySelector('.modal-backdrop') : null;
    if (stockBackdrop) {
        stockBackdrop.addEventListener('click', closeStockModal);
    }

    // Confirm delete
    confirmDelete.addEventListener('click', function() {
        if (!productToDelete) return;

        this.disabled = true;
        this.innerHTML = '<span class="spinner-small"></span> Deleting...';

        // Submit form to delete the product
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = `/products/${productToDelete}/delete/`;
        
        const csrfInput = document.createElement('input');
        csrfInput.type = 'hidden';
        csrfInput.name = 'csrfmiddlewaretoken';
        csrfInput.value = window.csrfToken;
        form.appendChild(csrfInput);
        
        document.body.appendChild(form);
        form.submit();
    });

    // Confirm stock adjustment
    confirmStock.addEventListener('click', function() {
        if (!productToAdjust) return;

        const type = adjustmentType.value;
        const quantity = parseInt(adjustmentQuantity.value) || 0;

        if (quantity < 0) {
            showToast('Quantity cannot be negative', 'error');
            return;
        }

        this.disabled = true;
        this.innerHTML = '<span class="spinner-small"></span> Updating...';

        // Submit form to adjust stock
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = `/products/${productToAdjust}/adjust-stock/`;
        
        const csrfInput = document.createElement('input');
        csrfInput.type = 'hidden';
        csrfInput.name = 'csrfmiddlewaretoken';
        csrfInput.value = window.csrfToken;
        form.appendChild(csrfInput);
        
        const typeInput = document.createElement('input');
        typeInput.type = 'hidden';
        typeInput.name = 'adjustment_type';
        typeInput.value = type;
        form.appendChild(typeInput);
        
        const quantityInput = document.createElement('input');
        quantityInput.type = 'hidden';
        quantityInput.name = 'quantity';
        quantityInput.value = quantity;
        form.appendChild(quantityInput);
        
        document.body.appendChild(form);
        form.submit();
    });
});
