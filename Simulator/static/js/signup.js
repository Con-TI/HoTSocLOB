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

// Handle login button click
document.getElementById('signup-button').addEventListener('click', signup_py);

async function signup_py() {
    const name = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const confirm_password = document.getElementById('confirm-password').value;
    
    response = await fetchDataFromDjango('/api/signup_py',{
    'name': name, 
    'password':password}
    ).then(message => {
    return message
    }).catch(error => {
    console.error('Failed to login/signup')
    })

    if (password === confirm_password){
        if (response['message'] === 'success'){
            // Store the username in sessionStorage so it's available on the next page
            sessionStorage.setItem('username', name);
            
            // Get current URL and remove "/login/" from the end
            const currentUrl = window.location.href;
            const baseUrl = currentUrl.replace('/signup/', '/');
            
            // Redirect to the base URL
            window.location.href = baseUrl + '/game/';
        } else {
            alert("Username already in use.")
        }
    } else {
        alert("Passwords do not match.")
    }

}