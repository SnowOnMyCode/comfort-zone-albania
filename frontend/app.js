const API_BASE = 'http://localhost:8000/api';

// Page navigation
function showPage(pageName) {
    // Hide all pages
    document.querySelectorAll('.page').forEach(page => {
        page.classList.add('hidden');
    });
    
    // Show selected page
    document.getElementById(`${pageName}-page`).classList.remove('hidden');
    
    // Load data for the page
    if (pageName === 'dashboard') {
        loadDashboard();
    } else if (pageName === 'products') {
        loadProducts();
    } else if (pageName === 'orders') {
        loadOrders();
    } else if (pageName === 'customers') {
        loadCustomers();
    }
}

// Dashboard
async function loadDashboard() {
    try {
        const response = await fetch(`${API_BASE}/analytics/dashboard`);
        const data = await response.json();
        
        document.getElementById('orders-today').textContent = data.orders_today;
        document.getElementById('total-revenue').textContent = `$${data.total_revenue.toFixed(2)}`;
        document.getElementById('total-products').textContent = data.total_products;
        
        // Chart
        if (data.top_products && data.top_products.length > 0) {
            const ctx = document.getElementById('topProductsChart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.top_products.map(p => p.name),
                    datasets: [{
                        label: 'Orders',
                        data: data.top_products.map(p => p.order_count),
                        backgroundColor: 'rgba(59, 130, 246, 0.5)',
                        borderColor: 'rgba(59, 130, 246, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

// Products
async function loadProducts() {
    try {
        const response = await fetch(`${API_BASE}/products/`);
        const products = await response.json();
        
        const tbody = document.getElementById('products-table-body');
        tbody.innerHTML = products.map(product => `
            <tr class="border-t">
                <td class="px-6 py-4">${product.sku}</td>
                <td class="px-6 py-4">${product.name}</td>
                <td class="px-6 py-4">${product.category}</td>
                <td class="px-6 py-4">$${product.current_price.toFixed(2)}</td>
                <td class="px-6 py-4">${product.stock_quantity}</td>
                <td class="px-6 py-4">
                    <button onclick="deleteProduct(${product.id})" class="text-red-500 hover:text-red-700">
                        Delete
                    </button>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error loading products:', error);
    }
}

async function searchProducts() {
    const searchTerm = document.getElementById('product-search').value;
    
    if (!searchTerm) {
        loadProducts();
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/products/search/${searchTerm}`);
        const products = await response.json();
        
        const tbody = document.getElementById('products-table-body');
        tbody.innerHTML = products.map(product => `
            <tr class="border-t">
                <td class="px-6 py-4">${product.sku}</td>
                <td class="px-6 py-4">${product.name}</td>
                <td class="px-6 py-4">${product.category}</td>
                <td class="px-6 py-4">$${product.current_price.toFixed(2)}</td>
                <td class="px-6 py-4">${product.stock_quantity}</td>
                <td class="px-6 py-4">
                    <button onclick="deleteProduct(${product.id})" class="text-red-500 hover:text-red-700">
                        Delete
                    </button>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error searching products:', error);
    }
}

async function deleteProduct(id) {
    if (!confirm('Are you sure you want to delete this product?')) {
        return;
    }
    
    try {
        await fetch(`${API_BASE}/products/${id}`, {
            method: 'DELETE'
        });
        loadProducts();
    } catch (error) {
        console.error('Error deleting product:', error);
    }
}

// Bulk Price Update
async function handleBulkUpdate(event) {
    event.preventDefault();
    
    const keyword = document.getElementById('bulk-keyword').value;
    const changeType = document.getElementById('bulk-change-type').value;
    const value = parseFloat(document.getElementById('bulk-value').value);
    
    try {
        const response = await fetch(`${API_BASE}/products/bulk-price-update?keyword=${keyword}&price_change_type=${changeType}&value=${value}`, {
            method: 'POST'
        });
        
        const result = await response.json();
        
        document.getElementById('bulk-result').innerHTML = `
            <div class="p-4 bg-green-100 border border-green-400 text-green-700 rounded">
                ✓ Updated ${result.updated} products matching "${result.keyword}"
            </div>
        `;
        
        // Clear after 3 seconds
        setTimeout(() => {
            document.getElementById('bulk-result').innerHTML = '';
        }, 3000);
    } catch (error) {
        console.error('Error updating prices:', error);
        document.getElementById('bulk-result').innerHTML = `
            <div class="p-4 bg-red-100 border border-red-400 text-red-700 rounded">
                Error updating prices
            </div>
        `;
    }
}

// Orders
async function loadOrders() {
    try {
        const response = await fetch(`${API_BASE}/orders/`);
        const orders = await response.json();
        
        const tbody = document.getElementById('orders-table-body');
        tbody.innerHTML = orders.map(order => `
            <tr class="border-t">
                <td class="px-6 py-4">${order.order_number}</td>
                <td class="px-6 py-4">${order.customer ? order.customer.name : 'N/A'}</td>
                <td class="px-6 py-4">
                    <span class="px-2 py-1 rounded text-sm ${getStatusColor(order.status)}">
                        ${order.status}
                    </span>
                </td>
                <td class="px-6 py-4">$${order.total_amount.toFixed(2)}</td>
                <td class="px-6 py-4">${new Date(order.created_at).toLocaleDateString()}</td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error loading orders:', error);
    }
}

function getStatusColor(status) {
    const colors = {
        'pending': 'bg-yellow-100 text-yellow-800',
        'processing': 'bg-blue-100 text-blue-800',
        'shipped': 'bg-purple-100 text-purple-800',
        'delivered': 'bg-green-100 text-green-800',
        'cancelled': 'bg-red-100 text-red-800'
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
}

// Customers
async function loadCustomers() {
    try {
        const response = await fetch(`${API_BASE}/customers/`);
        const customers = await response.json();
        
        const tbody = document.getElementById('customers-table-body');
        tbody.innerHTML = customers.map(customer => `
            <tr class="border-t">
                <td class="px-6 py-4">${customer.name}</td>
                <td class="px-6 py-4">
                    <span class="px-2 py-1 rounded text-sm ${getCustomerTypeColor(customer.type)}">
                        ${customer.type}
                    </span>
                </td>
                <td class="px-6 py-4">${customer.email}</td>
                <td class="px-6 py-4">${customer.phone}</td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error loading customers:', error);
    }
}

function getCustomerTypeColor(type) {
    const colors = {
        'hotel': 'bg-blue-100 text-blue-800',
        'hairdresser': 'bg-purple-100 text-purple-800',
        'pharmacy': 'bg-green-100 text-green-800'
    };
    return colors[type] || 'bg-gray-100 text-gray-800';
}

// Initialize - load dashboard on page load
document.addEventListener('DOMContentLoaded', () => {
    loadDashboard();
});
