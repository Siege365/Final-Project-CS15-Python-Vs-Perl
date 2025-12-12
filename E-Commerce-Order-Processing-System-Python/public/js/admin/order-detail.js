/**
 * Admin Order Detail
 * Status update and print functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    // Update status
    const updateBtn = document.getElementById('update-status-btn');
    const statusSelect = document.getElementById('update-status');

    if (updateBtn) {
        updateBtn.addEventListener('click', function() {
            const newStatus = statusSelect.value;
            
            this.disabled = true;
            this.innerHTML = '<span class="spinner-small"></span> Updating...';

            fetch(window.orderUrls.updateStatus, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': window.csrfToken
                },
                body: JSON.stringify({
                    order_id: window.orderId,
                    status: newStatus
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    alert(data.message || 'Failed to update status');
                    this.disabled = false;
                    this.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path><polyline points="17 21 17 13 7 13 7 21"></polyline></svg> Update';
                }
            })
            .catch(() => {
                alert('An error occurred');
                this.disabled = false;
            });
        });
    }

    // Print invoice
    const printBtn = document.getElementById('print-order');
    if (printBtn) {
        printBtn.addEventListener('click', function() {
            window.print();
        });
    }
});
