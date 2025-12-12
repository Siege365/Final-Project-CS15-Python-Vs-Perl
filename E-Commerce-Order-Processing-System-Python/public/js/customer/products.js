/**
 * Products Page - Customer
 * Handles add to cart, infinite scroll, and product interactions
 */

// DEBUG: This should appear immediately
console.log('=== PRODUCTS PAGE SCRIPT LOADED ===');
console.log('Timestamp:', new Date().toISOString());

document.addEventListener('DOMContentLoaded', function() {
    console.log('=== DOM CONTENT LOADED ===');
    
    // Debug: Check if buttons exist
    const addToCartBtns = document.querySelectorAll('.add-to-cart-btn');
    console.log('Found Add to Cart buttons:', addToCartBtns.length);
    
    // Track loaded product IDs to prevent duplicates
    const loadedProductIds = new Set();
    document.querySelectorAll('.product-card[data-product-id]').forEach(card => {
        loadedProductIds.add(parseInt(card.dataset.productId));
    });

    // Add to Cart functionality
    document.querySelectorAll('.add-to-cart-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            addToCart(this.dataset.productId, this);
        });
    });

    // Infinite scroll variables
    let isLoading = false;
    let hasMore = document.getElementById('infinite-scroll-status')?.dataset.hasMore === 'true';
    let nextPage = document.getElementById('infinite-scroll-status')?.dataset.nextPage;

    // Show end message if no more products on initial load
    if (!hasMore && document.querySelectorAll('.product-card').length > 0) {
        document.getElementById('end-of-products').style.display = 'block';
    }

    // Infinite scroll implementation
    window.addEventListener('scroll', function() {
        if (isLoading || !hasMore) return;
        
        const scrollPosition = window.innerHeight + window.scrollY;
        const documentHeight = document.documentElement.scrollHeight;
        
        // Load more when user is within 200px of bottom
        if (scrollPosition >= documentHeight - 200) {
            isLoading = true;
            loadMoreProducts(nextPage);
        }
    });

    function loadMoreProducts(page) {
        if (!page) return;
        
        const statusEl = document.getElementById('infinite-scroll-status');
        const endEl = document.getElementById('end-of-products');
        
        statusEl.style.display = 'block';

        const urlParams = new URLSearchParams(window.location.search);
        urlParams.set('page', page);
        urlParams.set('ajax', '1');

        fetch(window.productsUrls.products + '?' + urlParams.toString())
            .then(response => response.json())
            .then(data => {
                const grid = document.getElementById('products-grid');
                
                // Append new products (filter duplicates)
                data.products.forEach(product => {
                    if (!loadedProductIds.has(product.id)) {
                        loadedProductIds.add(product.id);
                        grid.insertAdjacentHTML('beforeend', createProductCard(product));
                    }
                });

                // Re-attach event listeners to new buttons
                grid.querySelectorAll('.add-to-cart-btn:not([data-attached])').forEach(btn => {
                    btn.setAttribute('data-attached', 'true');
                    btn.addEventListener('click', function() {
                        addToCart(this.dataset.productId, this);
                    });
                });

                // Update state
                hasMore = data.has_more;
                nextPage = data.next_page;
                statusEl.dataset.hasMore = hasMore ? 'true' : 'false';
                statusEl.dataset.nextPage = nextPage || '';
                
                statusEl.style.display = 'none';
                
                if (!hasMore) {
                    endEl.style.display = 'block';
                }
                
                isLoading = false;
            })
            .catch(error => {
                statusEl.style.display = 'none';
                showToast('Failed to load more products', 'error');
                isLoading = false;
            });
    }
});

function addToCart(productId, button) {
    console.log('Add to Cart clicked for product:', productId);
    
    const originalText = button.innerHTML;
    button.innerHTML = '<span class="spinner-small"></span> Adding...';
    button.disabled = true;

    // Get CSRF token from cookie as backup
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    const csrfToken = window.csrfToken || getCookie('csrftoken');
    console.log('Using CSRF token:', csrfToken ? 'Found' : 'Not found');
    
    const apiUrl = window.productsUrls.apiCartAdd;
    console.log('API URL:', apiUrl);

    fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({
            product_id: productId,
            quantity: 1
        }),
        credentials: 'same-origin'
    })
    .then(response => {
        console.log('Response status:', response.status);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Response data:', data);
        if (data.success) {
            // Update cart badge in topbar and sidebar
            updateCartBadge(data.cart_count);

            // Show success feedback
            button.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg> Added!';
            button.classList.add('btn-success');

            // Show toast notification with product name
            const productCard = button.closest('.product-card');
            const productName = productCard ? productCard.querySelector('.product-name').textContent : 'Product';
            showToast(`${productName} added to cart!`, 'success', 'Added to Cart');

            setTimeout(() => {
                button.innerHTML = originalText;
                button.classList.remove('btn-success');
                button.disabled = false;
            }, 1500);
        } else {
            button.innerHTML = originalText;
            button.disabled = false;
            showToast(data.message || 'Failed to add to cart', 'error', 'Error');
        }
    })
    .catch(error => {
        console.error('Add to cart error:', error);
        button.innerHTML = originalText;
        button.disabled = false;
        showToast('An error occurred: ' + error.message, 'error', 'Error');
    });
}

function createProductCard(product) {
    const stockBadge = product.stock <= 5 && product.stock > 0 
        ? `<span class="product-badge low-stock">Only ${product.stock} left!</span>`
        : product.stock === 0 
            ? `<span class="product-badge out-of-stock">Out of Stock</span>`
            : '';

    const addButton = product.stock > 0
        ? `<button class="btn btn-sm btn-primary add-to-cart-btn" data-product-id="${product.id}">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="9" cy="21" r="1"></circle>
                <circle cx="20" cy="21" r="1"></circle>
                <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
            </svg>
            Add to Cart
           </button>`
        : `<button class="btn btn-sm" disabled>Out of Stock</button>`;

    return `
        <div class="product-card" data-product-id="${product.id}">
            <div class="product-image">
                ${product.image_url 
                    ? `<img src="${product.image_url}" alt="${product.name}" loading="lazy">`
                    : `<div class="product-placeholder">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                            <circle cx="8.5" cy="8.5" r="1.5"></circle>
                            <polyline points="21 15 16 10 5 21"></polyline>
                        </svg>
                       </div>`
                }
                ${stockBadge}
            </div>
            <div class="product-info">
                <span class="product-category">${product.category}</span>
                <h3 class="product-name">${product.name}</h3>
                <p class="product-description">${product.description}</p>
                <div class="product-footer">
                    <span class="product-price">$${parseFloat(product.price).toFixed(2)}</span>
                    ${addButton}
                </div>
            </div>
        </div>
    `;
}
