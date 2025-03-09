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
    qIndex = Math.floor(index/2) % qs.question.length
    document.getElementById("questions").textContent = qs.question[qIndex];
}

async function update_answer(index) {
    const ans = await fetchDataFromDjango('api/answers_py',{});
    console.log(ans)
    if(index%2 == 1){
        aIndex = ((index-1)/2) % ans.answer.length
        document.getElementById("answers").textContent = ans.answer[aIndex];
    } else{
        document.getElementById("answers").textContent = 'Answer not yet released - gain you edge';
    }

}

let refreshIntervalquestion;
let refreshCounter = 0;

function startAutoRefreshQ() {
    // Clear any existing interval first
    stopAutoRefreshQ();
    
    // Immediately fetch q and a
    update_question(refreshCounter);
    update_answer(refreshCounter)
    
    // Then set up the interval
    refreshIntervalquestion = setInterval(() => {
        refreshCounter++;
        update_question(refreshCounter);
        update_answer(refreshCounter)
    }, 5000); // 7200000 milliseconds = 2 hours, 2 time steps for q, 1 for a
    
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
