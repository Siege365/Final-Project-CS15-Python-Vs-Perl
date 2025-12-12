/**
 * Order Detail - Customer
 * Handles order cancellation with improved UX
 */

document.addEventListener('DOMContentLoaded', function() {
    const cancelBtn = document.getElementById('cancel-order-btn');
    const modal = document.getElementById('cancel-order-modal');
    const modalBackdrop = modal?.querySelector('.cancel-modal-backdrop');
    const modalCancelBtn = document.getElementById('modal-cancel-btn');
    const modalConfirmBtn = document.getElementById('modal-confirm-btn');

    // Open cancel modal
    if (cancelBtn) {
        cancelBtn.addEventListener('click', function() {
            if (modal) {
                modal.classList.add('show');
                document.body.style.overflow = 'hidden';
            }
        });
    }

    // Close modal functions
    function closeModal() {
        if (modal) {
            modal.classList.remove('show');
            document.body.style.overflow = '';
        }
    }

    if (modalCancelBtn) {
        modalCancelBtn.addEventListener('click', closeModal);
    }

    if (modalBackdrop) {
        modalBackdrop.addEventListener('click', closeModal);
    }

    // Confirm cancellation
    if (modalConfirmBtn) {
        modalConfirmBtn.addEventListener('click', function() {
            const orderId = window.orderId;
            const originalText = this.innerHTML;
            
            // Disable buttons and show loading
            this.disabled = true;
            modalCancelBtn.disabled = true;
            this.innerHTML = '<span class="spinner-small"></span> Cancelling...';

            fetch(window.orderUrls.cancelOrder, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': window.csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({ order_id: orderId })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data && data.success) {
                    closeModal();
                    
                    // Show success toast
                    if (typeof showToast === 'function') {
                        showToast('Order cancelled successfully', 'success', 'Success');
                    }
                    
                    // Reload page after short delay
                    setTimeout(() => {
                        location.reload();
                    }, 1500);
                } else {
                    throw new Error(data?.message || 'Failed to cancel order');
                }
            })
            .catch(error => {
                console.error('Cancel order error:', error);
                
                // Show error toast
                if (typeof showToast === 'function') {
                    showToast(error.message || 'An error occurred while cancelling the order', 'error', 'Error');
                } else {
                    alert(error.message || 'An error occurred');
                }
                
                // Re-enable buttons
                this.disabled = false;
                modalCancelBtn.disabled = false;
                this.innerHTML = originalText;
            });
        });
    }

    // Handle escape key to close modal
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal && modal.classList.contains('show')) {
            closeModal();
        }
    });
});
