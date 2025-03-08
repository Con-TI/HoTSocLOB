document.addEventListener('DOMContentLoaded', function() {
    // Fetch current user stats

    // Fetch orderbook summary

    // Initialize/Update the price chart + add to price history

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

    // Periodic refresh (3 seconds)
});