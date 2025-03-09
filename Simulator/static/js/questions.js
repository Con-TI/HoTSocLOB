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

async function update_question() {
    const qs = await fetchDataFromDjango('api/questions_py',{});
    document.getElementById("questions").textContent = qs.question;
}

async function update_answer() {
    const ans = await fetchDataFromDjango('api/answers_py',{});
    document.getElementById("answers").textContent = ans.answer;

}

let refreshIntervalquestion;

function startAutoRefreshQ() {
    // Clear any existing interval first
    stopAutoRefreshQ();
    
    // Immediately fetch q and a
    update_question();
    update_answer();
    
    // Then set up the interval
    refreshIntervalquestion = setInterval(() => {
        update_question();
        update_answer();
    }, 500); // 5000ms=5 seconds
    
    console.log('Auto-refresh started: updating question and answer every 2 hours');
}

function stopAutoRefreshQ() {
    if (refreshIntervalquestion) {
        clearInterval(refreshIntervalquestion);
        refreshIntervalquestion = null;
        console.log('Question and answer auto-refresh stopped');
    }
}

document.addEventListener('DOMContentLoaded', function() {
    startAutoRefreshQ();
});
