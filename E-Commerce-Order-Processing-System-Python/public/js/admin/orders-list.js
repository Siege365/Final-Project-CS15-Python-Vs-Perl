/**
 * Admin Orders List
 * Bulk actions and kebab menu actions
 */

document.addEventListener('DOMContentLoaded', function() {
    const selectAll = document.getElementById('select-all');
    const checkboxes = document.querySelectorAll('.order-checkbox');
    const bulkActions = document.getElementById('bulk-actions');

    // Kebab menu functionality
    document.querySelectorAll('.kebab-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            const menu = this.closest('.kebab-menu');
            const wasOpen = menu.classList.contains('open');
            
            // Close all other menus
            document.querySelectorAll('.kebab-menu.open').forEach(m => {
                if (m !== menu) m.classList.remove('open');
            });
            
            menu.classList.toggle('open', !wasOpen);
        });
    });

    // Close kebab menus when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.kebab-menu')) {
            document.querySelectorAll('.kebab-menu.open').forEach(menu => {
                menu.classList.remove('open');
            });
        }
    });

    // Status Change Modal
    const statusModal = document.getElementById('status-modal');
    const statusModalClose = document.getElementById('status-modal-close');
    const statusCancel = document.getElementById('status-cancel');
    const statusConfirm = document.getElementById('status-confirm');
    const newStatusSelect = document.getElementById('new-status');
    let currentOrderId = null;

    function openStatusModal(orderId, orderNumber, currentStatus) {
        currentOrderId = orderId;
        document.getElementById('status-order-number').textContent = orderNumber;
        newStatusSelect.value = currentStatus;
        statusModal.classList.add('show');
    }

    function closeStatusModal() {
        statusModal.classList.remove('show');
        currentOrderId = null;
    }

    statusModalClose.addEventListener('click', closeStatusModal);
    statusCancel.addEventListener('click', closeStatusModal);
    statusModal.querySelector('.modal-backdrop').addEventListener('click', closeStatusModal);

    statusConfirm.addEventListener('click', function() {
        if (!currentOrderId) return;

        const newStatus = newStatusSelect.value;
        this.disabled = true;
        this.innerHTML = '<span class="spinner-small"></span> Updating...';

        fetch(window.orderUrls.updateStatus, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': window.csrfToken
            },
            body: JSON.stringify({
                order_id: currentOrderId,
                status: newStatus
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showToast('Order status updated successfully', 'success');
                setTimeout(() => location.reload(), 500);
            } else {
                showToast(data.message || 'Failed to update status', 'error');
                this.disabled = false;
                this.innerHTML = 'Update Status';
            }
        })
        .catch(() => {
            showToast('An error occurred', 'error');
            this.disabled = false;
            this.innerHTML = 'Update Status';
        });
    });

    // Delete Order Modal
    const deleteModal = document.getElementById('delete-order-modal');
    const deleteModalClose = document.getElementById('delete-order-modal-close');
    const deleteCancel = document.getElementById('delete-order-cancel');
    const deleteConfirm = document.getElementById('delete-order-confirm');
    let deleteOrderId = null;

    function openDeleteModal(orderId, orderNumber) {
        deleteOrderId = orderId;
        document.getElementById('delete-order-number').textContent = orderNumber;
        deleteModal.classList.add('show');
    }

    function closeDeleteModal() {
        deleteModal.classList.remove('show');
        deleteOrderId = null;
    }

    deleteModalClose.addEventListener('click', closeDeleteModal);
    deleteCancel.addEventListener('click', closeDeleteModal);
    deleteModal.querySelector('.modal-backdrop').addEventListener('click', closeDeleteModal);

    deleteConfirm.addEventListener('click', function() {
        if (!deleteOrderId) return;

        this.disabled = true;
        this.innerHTML = '<span class="spinner-small"></span> Deleting...';

        const form = document.createElement('form');
        form.method = 'POST';
        form.action = window.orderUrls.deleteOrder + deleteOrderId + '/delete/';
        
        const csrfInput = document.createElement('input');
        csrfInput.type = 'hidden';
        csrfInput.name = 'csrfmiddlewaretoken';
        csrfInput.value = window.csrfToken;
        form.appendChild(csrfInput);
        
        document.body.appendChild(form);
        form.submit();
    });

    // Attach event listeners to kebab menu items
    document.querySelectorAll('.status-change-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const orderId = this.dataset.orderId;
            const currentStatus = this.dataset.currentStatus;
            const orderNumber = this.closest('tr').querySelector('td:nth-child(2)').textContent.trim();
            openStatusModal(orderId, orderNumber, currentStatus);
        });
    });

    document.querySelectorAll('.delete-order-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const orderId = this.dataset.orderId;
            const orderNumber = this.dataset.orderNumber;
            openDeleteModal(orderId, orderNumber);
        });
    });

    if (selectAll) {
        // Select all functionality
        selectAll.addEventListener('change', function() {
            checkboxes.forEach(cb => cb.checked = this.checked);
            updateBulkActions();
        });

        checkboxes.forEach(cb => {
            cb.addEventListener('change', updateBulkActions);
        });

        function updateBulkActions() {
            const checked = document.querySelectorAll('.order-checkbox:checked');
            bulkActions.style.display = checked.length > 0 ? 'flex' : 'none';
        }

        // Bulk action
        document.getElementById('apply-bulk-action').addEventListener('click', function() {
            const action = document.getElementById('bulk-action').value;
            if (!action) {
                alert('Please select an action');
                return;
            }

            const selectedOrders = Array.from(document.querySelectorAll('.order-checkbox:checked'))
                .map(cb => cb.value);

            if (selectedOrders.length === 0) {
                alert('Please select at least one order');
                return;
            }

            if (action === 'cancelled' && !confirm('Are you sure you want to cancel the selected orders?')) {
                return;
            }

            this.disabled = true;
            this.innerHTML = '<span class="spinner-small"></span>';

            fetch(window.orderUrls.bulkUpdate, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': window.csrfToken
                },
                body: JSON.stringify({
                    order_ids: selectedOrders,
                    status: action
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    alert(data.message || 'Failed to update orders');
                    this.disabled = false;
                    this.innerHTML = 'Apply';
                }
            })
            .catch(() => {
                alert('An error occurred');
                this.disabled = false;
                this.innerHTML = 'Apply';
            });
        });
    }
});
