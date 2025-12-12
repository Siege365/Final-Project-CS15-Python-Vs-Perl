/**
 * Admin Reports
 * Chart.js visualization and date range filtering
 */

document.addEventListener('DOMContentLoaded', function() {
    // Date range toggle
    const periodSelect = document.getElementById('period');
    const dateFromGroup = document.getElementById('date-from-group');
    const dateToGroup = document.getElementById('date-to-group');

    if (periodSelect) {
        periodSelect.addEventListener('change', function() {
            if (this.value === 'custom') {
                dateFromGroup.style.display = 'block';
                dateToGroup.style.display = 'block';
            } else {
                dateFromGroup.style.display = 'none';
                dateToGroup.style.display = 'none';
            }
        });
    }

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

    // Category Chart
    const categoryCtx = document.getElementById('category-chart');
    if (categoryCtx && window.chartData) {
        new Chart(categoryCtx, {
            type: 'doughnut',
            data: {
                labels: window.chartData.category_labels,
                datasets: [{
                    data: window.chartData.category_data,
                    backgroundColor: [
                        'rgb(99, 102, 241)',
                        'rgb(34, 197, 94)',
                        'rgb(245, 158, 11)',
                        'rgb(239, 68, 68)',
                        'rgb(139, 92, 246)',
                        'rgb(59, 130, 246)'
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

    // Status Chart
    const statusCtx = document.getElementById('status-chart');
    if (statusCtx && window.chartData) {
        new Chart(statusCtx, {
            type: 'doughnut',
            data: {
                labels: ['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled'],
                datasets: [{
                    data: window.chartData.status_data,
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
