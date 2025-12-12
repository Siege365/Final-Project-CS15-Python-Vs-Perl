/**
 * Admin Dashboard
 * Chart.js integration for revenue and orders visualization
 */

document.addEventListener('DOMContentLoaded', function() {
    // Revenue Chart
    const revenueCtx = document.getElementById('revenue-chart');
    if (revenueCtx && window.chartData) {
        new Chart(revenueCtx, {
            type: 'line',
            data: {
                labels: window.chartData.revenue_labels,
                datasets: [{
                    label: 'Revenue',
                    data: window.chartData.revenue_data,
                    borderColor: 'rgb(99, 102, 241)',
                    backgroundColor: 'rgba(99, 102, 241, 0.1)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '$' + value;
                            }
                        }
                    }
                }
            }
        });
    }

    // Orders Chart
    const ordersCtx = document.getElementById('orders-chart');
    if (ordersCtx && window.chartData) {
        new Chart(ordersCtx, {
            type: 'doughnut',
            data: {
                labels: ['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled'],
                datasets: [{
                    data: window.chartData.orders_by_status,
                    backgroundColor: [
                        'rgb(245, 158, 11)',
                        'rgb(59, 130, 246)',
                        'rgb(139, 92, 246)',
                        'rgb(34, 197, 94)',
                        'rgb(239, 68, 68)'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
});
