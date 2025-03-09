let refreshInterval;
function username_update(){
    const name = sessionStorage.getItem('username');
    disp = document.getElementById('user-display')
    disp.textContent = name
}

function startAutoRefresh() {
    // Clear any existing interval first
    stopAutoRefresh();
    
    // Immediately fetch orders
    updateUserStats();
    get_current_orderbook();
    
    // Then set up the interval
    refreshInterval = setInterval(() => {
        updateUserStats();
        get_current_orderbook();
    }, 2500); // 5000 milliseconds = 5 seconds
    
    console.log('Auto-refresh started: updating orders every 2.5 seconds');
}

function stopAutoRefresh() {
    if (refreshInterval) {
        clearInterval(refreshInterval);
        refreshInterval = null;
        console.log('Orders auto-refresh stopped');
    }
}

async function get_current_orderbook(){
    data = await fetchDataFromDjango('/api/fetch_orderbook')
    .then(data => {
        return data
    }).catch(error => {
        console.error('Error fetching data from Django:', error);
        throw error;
    });

    // Get the table bodies
    const buyTableBody = document.querySelector("#buy-orders table tbody");
    const sellTableBody = document.querySelector("#sell-orders table tbody");
    
    // Update buy orders (bids)
    if (buyTableBody) {
        buyTableBody.innerHTML = '';
        
        if (!data.bids || data.bids.length === 0) {
            const noDataRow = document.createElement('tr');
            noDataRow.innerHTML = '<td colspan="2" class="text-center">No orders</td>';
            buyTableBody.appendChild(noDataRow);
        } else {
            const sortedBids = [...data.bids].sort((a, b) => b.price - a.price);
            // Then create rows for each bid
            sortedBids.forEach(order => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${order.quantity || ''}</td>
                    <td>${order.price || ''}</td>
                `;
                buyTableBody.appendChild(row);
            });
        }
    }
    
    // Update sell orders (asks)
    if (sellTableBody) {
        sellTableBody.innerHTML = '';
        
        if (!data.asks || data.asks.length === 0) {
            const noDataRow = document.createElement('tr');
            noDataRow.innerHTML = '<td colspan="2" class="text-center">No orders</td>';
            sellTableBody.appendChild(noDataRow);
        } else {
            // Add each order to the table - make sure to match the HTML order
            // Your HTML has "Ask" first, then "Ask Quantity"
            const sortedAsks = [...data.asks].sort((a, b) => a.price - b.price);
            // Then create rows for each bid
            sortedAsks.forEach(order => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${order.price || ''}</td>
                    <td>${order.quantity || ''}</td>
                `;
                sellTableBody.appendChild(row);
            });
        }
    }

}

async function updateUserStats() {
    try {
        username_elem = document.getElementById('user-display')
        const username = username_elem.textContent;
        const statsData = await fetchDataFromDjango('/api/update_userstats', {
            'user': username
        });

        // Check if we got a valid response
        if (statsData.message === 'error') {
            console.log(statsData)
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
    const equityElement = document.getElementById('equity-display');
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
    
    if (data.pending_orders && Array.isArray(data.pending_orders)) {
        const tableBody = document.getElementById('order-list');
        if (tableBody) {
            // Clear existing rows
            tableBody.innerHTML = '';

            const columns = document.createElement('tr');
            columns.innerHTML = `
                <th>Price</th>
                <th>Quantity</th>
            `
            tableBody.appendChild(columns)
            
            // Check if we have orders
            if (data.pending_orders.length === 0) {
                const noDataRow = document.createElement('tr');
                noDataRow.innerHTML = '<td colspan="5" class="text-center">No pending orders</td>';
                tableBody.appendChild(noDataRow);
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
    
    if (data.positions && Array.isArray(data.positions)) {
        const tableBody2 = document.getElementById('positions-list');
        if (tableBody2) {
            // Clear existing rows
            tableBody2.innerHTML = '';

            const columns2 = document.createElement('tr');
            columns2.innerHTML = `
                <th>Price</th>
                <th>Quantity</th>
            `
            tableBody2.appendChild(columns2)
            
            // Check if we have positions
            if (data.positions.length === 0) {
                const noDataRow = document.createElement('tr');
                noDataRow.innerHTML = '<td colspan="5" class="text-center">No positions</td>';
                tableBody2.appendChild(noDataRow);
                return;
            }

            // Add each positions to the table
            data.positions.forEach(pos => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${pos.price || ''}</td>
                    <td>${pos.quantity || ''}</td>
                `;
                tableBody2.appendChild(row);
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
async function add_buy_order() {
    // TODO: Get values for quantity, price, user
    const user = document.getElementById('user-display').textContent;
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
async function add_sell_order() {
    const user = document.getElementById('user-display').textContent;
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

// Handle clear pending orders click
async function clear_pending_orders() {
    const user = document.getElementById('user-display').textContent;
    fetchDataFromDjango('/api/clear_pending_orders',{
        'user': user,
    }).then(data => {
        console.log('Deleted Orders')
    }).catch(error => {
        console.error("No pending orders")
    })
}

// Periodic refresh (3 seconds)

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('buy-button').addEventListener('click', add_buy_order);
    document.getElementById('sell-button').addEventListener('click', add_sell_order);
    document.getElementById('clear-pending-button').addEventListener('click', clear_pending_orders);
    username_update();
    startAutoRefresh();
});