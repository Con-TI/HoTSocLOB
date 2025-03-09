let priceChart;

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

async function update_price_chart(){
    const data = await fetchDataFromDjango('api/chart_py',{});
    
    priceChart.data.labels = data.labels;
    priceChart.data.datasets[0].data = data.prices;
    priceChart.update();
}

async function plot_new_prices(){
    const data = await fetchDataFromDjango('api/chart_py',{});
    const ctx = document.getElementById('midprice-chart').getContext('2d');
    priceChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: data.labels,
          datasets: [{
            label: 'Stock Price',
            data: data.prices,
            borderColor: 'rgb(75, 192, 192)',
            backgroundColor: 'rgba(75, 192, 192, 0.1)',
            borderWidth: 2,
            tension: 0.1,
            fill: true
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: false
            }
          },
          plugins: {
            tooltip: {
              callbacks: {
                label: function(context) {
                  return `$${context.raw.toFixed(2)}`;
                }
              }
            }
          }
        }
      });
}

let refreshIntervalchart;

function startAutoRefresh2() {
    // Clear any existing interval first
    stopAutoRefresh2();
    
    // Immediately fetch orders
    plot_new_prices();
    
    // Then set up the interval
    refreshIntervalchart = setInterval(() => {
        update_price_chart();
    }, 2500); // 5000 milliseconds = 5 seconds
    
    console.log('Auto-refresh started: updating chart every 2.5 seconds');
}

function stopAutoRefresh2() {
    if (refreshIntervalchart) {
        clearInterval(refreshIntervalchart);
        refreshIntervalchart = null;
        console.log('Chart auto-refresh stopped');
    }
}

document.addEventListener('DOMContentLoaded', function() {
    startAutoRefresh2();
});
