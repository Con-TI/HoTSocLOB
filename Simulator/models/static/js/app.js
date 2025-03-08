document.addEventListener('DOMContentLoaded', function() {
    let RefreshInterval;
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
    // Fetch current user stats

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
            console.error('Error adding buy order:', error);
        });

    }

    // Function to fetch pending orders
    async function fetchPendingOrders() {
        // TODO: Send request to views. Handle errors
        const user = document.getElementById('user-display').value;
        fetchDataFromDjango('/api/fetch_pending_orders', {
        'user': user,
        }).then(data => {
            console.log('Data received:', data)
            return data;
        }).catch(error => {
            console.error('Error adding buy order:', error);
        });
    }

    // 

    // Periodic refresh (3 seconds)
});