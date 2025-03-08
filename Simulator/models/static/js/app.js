let refreshInterval;
function startAutoRefresh() {
    // Clear any existing interval first
    stopAutoRefresh();
    
    // Immediately fetch orders
    updateUserStats();
    
    // Then set up the interval
    refreshInterval = setInterval(() => {
        updateUserStats();
    }, 5000); // 5000 milliseconds = 5 seconds
    
    console.log('Auto-refresh started: updating orders every 5 seconds');
}

function stopAutoRefresh() {
    if (refreshInterval) {
        clearInterval(refreshInterval);
        refreshInterval = null;
        console.log('Orders auto-refresh stopped');
    }
}

async function updateUserStats() {
    try {
        const username = document.getElementById('user-display').value;
        
        const statsData = await fetchDataFromDjango('/api/update_userstats', {
            'user': username
        });

        // Check if we got a valid response
        if (statsData.message === 'error') {
            console.error('Error fetching user stats');
            return;
        }
        
        // Update the DOM with fetched stats
        displayUserStats(statsData);
        
    } catch (error) {
        console.error('Failed to update user stats:', error);
    }
}


// Function to display the user stats in the UI
function displayUserStats(data) {
    // Update equity
    const equityElement = document.getElementById('equit-display');
    if (equityElement) {
        equityElement.textContent = `$${data.equity.toFixed(2)}`;
    }
    
    // Update PnL
    const pnlElement = document.getElementById('realized-pnl-display');
    if (pnlElement) {
        const pnlValue = data.pnl;
        const pnlColor = pnlValue >= 0 ? 'text-success' : 'text-danger';
        pnlElement.textContent = `$${pnlValue.toFixed(2)}`;
        pnlElement.className = pnlColor;
    }
    
    // Update unrealized PnL
    const unrealPnlElement = document.getElementById('unrealized-pnl-display');
    if (unrealPnlElement) {
        const unrealPnlValue = data.unreal_pnl;
        const unrealPnlColor = unrealPnlValue >= 0 ? 'text-success' : 'text-danger';
        unrealPnlElement.textContent = `$${unrealPnlValue.toFixed(2)}`;
        unrealPnlElement.className = unrealPnlColor;
    }
    
    // If you want to also handle the pending orders from this endpoint
    // This could replace or supplement your existing pending orders function
    if (data.pending_orders && Array.isArray(data.pending_orders)) {
        const tableBody = document.getElementById('order-list');
        if (tableBody) {
            // Clear existing rows
            tableBody.innerHTML = '';
            
            // Check if we have orders
            if (data.pending_orders.length === 0) {
                const noDataRow = document.createElement('tr');
                noDataRow.innerHTML = '<td colspan="5" class="text-center">No pending orders</td>';
                tableBody.appendChild(noDataRow);
                return;
            }
            
            // Add each order to the table
            data.pending_orders.forEach(order => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${order.price || ''}</td>
                    <td>${order.quantity || ''}</td>
                `;
                tableBody.appendChild(row);
            });
        }
    }
}
function fetchDataFromDjango(endpoint, params = {}) {
    // Convert params object to URL parameters
    const queryString = new URLSearchParams(params).toString();
    const url = queryString ? `${endpoint}?${queryString}` : endpoint;
    
    // Send the GET request
    return fetch(url, {
        method: 'GET',
        headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
        },
        credentials: 'same-origin'  // Sends cookies with the request
    })
    .then(response => {
        if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();  // Parse JSON response
    })
    .catch(error => {
        console.error('Error fetching data from Django:', error);
        throw error;
    });
}    
// Fetch orderbook summary

// Initialize/Update the price chart + add to price history


// Handle buy button click
document.getElementById('buy-button').addEventListener('click', add_buy_order);
async function add_buy_order() {
    // TODO: Get values for quantity, price, user
    const user = document.getElementById('user-display').value;
    const price = document.getElementById('price').value;
    const quantity = document.getElementById('quantity').value;

    if (!price || !quantity) {
        alert('Please enter both price and quantity');
        return;
    }

    // TODO: Send request to views. Handle errors
    fetchDataFromDjango('/api/buy_order', {
        'user': user,
        'price': price,
        'quantity': quantity,
    }).then(data => {
        console.log('Data received:', data)
    }).catch(error => {
        console.error('Error adding buy order:', error);
    });
};

// Handle sell button click
document.getElementById('sell-button').addEventListener('click', add_sell_order);
async function add_sell_order() {
    const user = document.getElementById('user-display').value;
    const price = document.getElementById('price').value;
    const quantity = document.getElementById('quantity').value;

    if (!price || !quantity) {
        alert('Please enter both price and quantity');
        return;
    }

    // TODO: Send request to views. Handle errors
    fetchDataFromDjango('/api/sell_order', {
        'user': user,
        'price': price,
        'quantity': quantity,
    }).then(data => {
        console.log('Data received:', data)
    }).catch(error => {
        console.error('Error adding sell order:', error);
    });

}

// Periodic refresh (3 seconds)

document.addEventListener('DOMContentLoaded', function() {
    startAutoRefresh();
});