document.addEventListener('DOMContentLoaded', function() {
    // Fetch current user stats

    // Fetch orderbook summary

    // Initialize/Update the price chart

    // Handle buy button click
    document.getElementById('buy-button').addEventListener('click', function() {
        // TODO: Get values for quantity, price, user
        const price = document.getElementById('price').value;
        const quantity = document.getElementById('quantity').value;

        if (!price || !quantity) {
            alert('Please enter both price and quantity');
            return;
        }

        // TODO: Send request to views. Handle errors

        fetch('/buy_order')

    });

    // Handle sell button click
    document.getElementById('sell-button').addEventListener('click', function() {
        // TODO: Get values for quantity and price
        const price = document.getElementById('price').value;
        const quantity = document.getElementById('quantity').value;

        if (!price || !quantity) {
            alert('Please enter both price and quantity');
            return;
        }

        // TODO: Send request to views. Handle errors

    });

    // Function to fetch pending orders
    function fetchPendingOrders() {
        fetch('/api/pending-orders/')
            .then(response => response.json())
            .then(data => {
                const orderList = document.querySelector('#order-list tbody');
                orderList.innerHTML = '';
                
                data.orders.forEach(order => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${order.price.toFixed(2)}</td>
                        <td>${order.quantity.toFixed(2)}</td>
                        <td>${order.order_type}</td>
                    `;
                    orderList.appendChild(row);
                });
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    // Function to fetch account info
    function fetchAccountInfo() {
        fetch('/api/account-info/')
            .then(response => response.json())
            .then(data => {
                document.getElementById('user-display').textContent = data.user;
                document.getElementById('equity-display').textContent = data.equity.toFixed(2);
                document.getElementById('unrealized-pnl-display').textContent = data.unrealized_pnl.toFixed(2);
                document.getElementById('realized-pnl-display').textContent = data.realized_pnl.toFixed(2);
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    // Function to fetch price history
    function fetchPriceHistory() {
        fetch('/api/price-history/')
            .then(response => response.json())
            .then(data => {
                // Update chart data
                priceChart.data.labels = data.prices.map(price => price.timestamp);
                priceChart.data.datasets[0].data = data.prices.map(price => price.midprice);
                priceChart.update();
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    // Helper function to get CSRF token
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

    // Periodic refresh (3 seconds)
});