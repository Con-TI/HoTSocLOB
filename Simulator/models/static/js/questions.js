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

async function update_question(index) {
    const qs = await fetchDataFromDjango('api/questions_py',{});
    qIndex = index % qs.question.length
    document.getElementById("questions").textContent = qs.question[qIndex];
}

let refreshIntervalquestion;
let refreshCounter = 0;

function startAutoRefreshQ() {
    // Clear any existing interval first
    stopAutoRefreshQ();
    
    // Immediately fetch orders
    update_question(refreshCounter);
    
    // Then set up the interval
    refreshIntervalquestion = setInterval(() => {
        refreshCounter++;
        update_question(refreshCounter);
    }, 5000); // 14400000 milliseconds = 4 hours
    
    console.log('Auto-refresh started: updating question every 4 hours');
}

function stopAutoRefreshQ() {
    if (refreshIntervalquestion) {
        clearInterval(refreshIntervalquestion);
        refreshIntervalquestion = null;
        console.log('Question auto-refresh stopped');
    }
}

document.addEventListener('DOMContentLoaded', function() {
    startAutoRefreshQ();
});
