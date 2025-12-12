/**
 * Shopping Cart Management
 * Handles cart operations: update quantity, remove items, checkout
 */

document.addEventListener('DOMContentLoaded', function() {
    // Quantity buttons
    document.querySelectorAll('.quantity-btn.minus').forEach(btn => {
        btn.addEventListener('click', () => updateQuantity(btn.dataset.productId, -1));
    });

    document.querySelectorAll('.quantity-btn.plus').forEach(btn => {
        btn.addEventListener('click', () => updateQuantity(btn.dataset.productId, 1));
    });

    // Quantity input change
    document.querySelectorAll('.quantity-input').forEach(input => {
        input.addEventListener('change', function() {
            setQuantity(this.dataset.productId, parseInt(this.value));
        });
    });

    // Remove buttons
    document.querySelectorAll('.cart-item-remove').forEach(btn => {
        btn.addEventListener('click', () => removeItem(btn.dataset.productId));
    });

    // Clear cart
    const clearCartBtn = document.getElementById('clear-cart-btn');
    if (clearCartBtn) {
        clearCartBtn.addEventListener('click', clearCart);
    }

    // Place order button - opens confirmation modal
    const placeOrderBtn = document.getElementById('place-order-btn');
    const confirmModal = document.getElementById('confirm-order-modal');
    const confirmModalClose = document.getElementById('confirm-modal-close');
    const cancelOrderBtn = document.getElementById('cancel-order-btn');
    const confirmOrderBtn = document.getElementById('confirm-order-btn');
    const modalBackdrop = confirmModal?.querySelector('.modal-backdrop');

    if (placeOrderBtn) {
        placeOrderBtn.addEventListener('click', () => {
            // Validate form first
            const form = document.getElementById('checkout-form');
            if (!form.checkValidity()) {
                form.reportValidity();
                return;
            }
            
            // Update confirmation modal with selected payment method
            const selectedPayment = document.querySelector('input[name="payment_method"]:checked');
            const paymentMethodText = selectedPayment ? selectedPayment.nextElementSibling.querySelector('span').textContent : 'Credit Card';
            document.getElementById('confirm-payment-method').textContent = paymentMethodText;
            
            // Show modal
            confirmModal.classList.add('show');
        });
    }

    if (confirmModalClose) {
        confirmModalClose.addEventListener('click', () => confirmModal.classList.remove('show'));
    }

    if (cancelOrderBtn) {
        cancelOrderBtn.addEventListener('click', () => confirmModal.classList.remove('show'));
    }

    if (modalBackdrop) {
        modalBackdrop.addEventListener('click', () => confirmModal.classList.remove('show'));
    }

    if (confirmOrderBtn) {
        confirmOrderBtn.addEventListener('click', handleCheckout);
    }
});

function updateQuantity(productId, delta) {
    const input = document.querySelector(`.quantity-input[data-product-id="${productId}"]`);
    const newQuantity = parseInt(input.value) + delta;
    
    if (newQuantity < 1) {
        removeItem(productId);
        return;
    }

    setQuantity(productId, newQuantity);
}

function setQuantity(productId, quantity) {
    fetch(window.cartUrls.update, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': window.csrfToken
        },
        body: JSON.stringify({
            product_id: productId,
            quantity: quantity
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data && data.success) {
            updateCartDisplay(data);
        } else {
            showToast(data?.message || 'Failed to update quantity', 'error');
        }
    })
    .catch(error => {
        console.error('Cart update error:', error);
        showToast('An error occurred while updating cart', 'error');
    });
}

function removeItem(productId) {
    const item = document.querySelector(`.cart-item[data-product-id="${productId}"]`);
    item.classList.add('removing');

    fetch(window.cartUrls.remove, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': window.csrfToken
        },
        body: JSON.stringify({ product_id: productId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            setTimeout(() => {
                item.remove();
                if (data.cart_count === 0) {
                    location.reload();
                } else {
                    updateCartDisplay(data);
                }
            }, 300);
        } else {
            item.classList.remove('removing');
            showToast(data.message || 'Failed to remove item', 'error');
        }
    })
    .catch(() => {
        item.classList.remove('removing');
        showToast('An error occurred', 'error');
    });
}

function clearCart() {
    if (!confirm('Are you sure you want to clear your cart?')) return;

    fetch(window.cartUrls.clear, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': window.csrfToken
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            showToast(data.message || 'Failed to clear cart', 'error');
        }
    })
    .catch(() => showToast('An error occurred', 'error'));
}

function updateCartDisplay(data) {
    // Update header cart count
    if (typeof updateCartBadge === 'function') {
        updateCartBadge(data.cart_count);
    }

    // Update summary
    const subtotalEl = document.getElementById('cart-subtotal');
    const taxEl = document.getElementById('cart-tax');
    const totalEl = document.getElementById('cart-total');
    const shippingEl = document.getElementById('cart-shipping');
    
    if (subtotalEl) subtotalEl.textContent = '$' + data.subtotal.toFixed(2);
    if (taxEl) taxEl.textContent = '$' + data.tax.toFixed(2);
    if (totalEl) totalEl.textContent = '$' + data.total.toFixed(2);

    // Update shipping
    if (shippingEl) {
        if (data.free_shipping) {
            shippingEl.innerHTML = '<span class="free-shipping">FREE</span>';
        } else {
            shippingEl.textContent = '$' + data.shipping.toFixed(2);
        }
    }

    // Update item subtotals
    if (data.items && Array.isArray(data.items)) {
        data.items.forEach(item => {
            const input = document.querySelector(`.quantity-input[data-product-id="${item.product_id}"]`);
            if (input) {
                input.value = item.quantity;
                const cartItem = input.closest('.cart-item');
                if (cartItem) {
                    const subtotalEl = cartItem.querySelector('.item-subtotal');
                    if (subtotalEl && item.subtotal !== undefined) {
                        subtotalEl.textContent = item.subtotal.toFixed(2);
                    }
                }
            }
        });
    }
}

function handleCheckout(e) {
    if (e) e.preventDefault();
    
    const confirmModal = document.getElementById('confirm-order-modal');
    const confirmBtn = document.getElementById('confirm-order-btn');
    const originalText = confirmBtn.innerHTML;
    confirmBtn.innerHTML = '<span class="spinner-small"></span> Processing...';
    confirmBtn.disabled = true;

    const form = document.getElementById('checkout-form');
    const formData = new FormData(form);

    fetch(window.cartUrls.checkout, {
        method: 'POST',
        headers: {
            'X-CSRFToken': window.csrfToken,
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            confirmModal.classList.remove('show');
            showToast('Order placed successfully!', 'success');
            setTimeout(() => {
                window.location.href = data.redirect || window.cartUrls.ordersPage;
            }, 1000);
        } else {
            confirmBtn.innerHTML = originalText;
            confirmBtn.disabled = false;
            confirmModal.classList.remove('show');
            showToast(data.message || 'Failed to place order', 'error');
        }
    })
    .catch(() => {
        confirmBtn.innerHTML = originalText;
        confirmBtn.disabled = false;
        confirmModal.classList.remove('show');
        showToast('An error occurred', 'error');
    });
}
