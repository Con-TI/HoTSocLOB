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
document.getElementById('login-button').addEventListener('click', login_py);

async function login_py() {
    const name = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    response = await fetchDataFromDjango('/api/login_py',{
    'name': name, 
    'password':password}
    ).then(message => {
    return message
    }).catch(error => {
    console.error('Failed to login/signup')
    })

    if (response['message'] === 'success'){
        // Store the username in sessionStorage so it's available on the next page
        sessionStorage.setItem('username', name);
        
        // Get current URL and remove "/login/" from the end
        const currentUrl = window.location.href;
        const baseUrl = currentUrl.replace('/login/', '/');
        
        // Redirect to the base URL
        window.location.href = baseUrl;
    } else {
        alert("Invalid username or password")
    }

}