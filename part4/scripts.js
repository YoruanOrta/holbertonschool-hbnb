document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const priceFilter = document.getElementById('price-filter');
    const loginLink = document.getElementById('login-link');
    const logoutLink = document.getElementById('logout-link');
    const userInfo = document.getElementById('user-info');
    const addReview = document.getElementById('add-review');

    // Handle login form submission
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            await loginUser(email, password);
        });
    }

    // Setup logout functionality
    if (logoutLink) {
        logoutLink.addEventListener('click', (event) => {
            event.preventDefault();
            logoutUser();
        });
    }

    // Check if user is authenticated when the page loads
    updateAuthUI();

    // Populate and set up price filter dropdown
    if (priceFilter) {
        priceFilter.addEventListener('change', (event) => {
            const selectedPrice = event.target.value;
            filterPlacesByPrice(selectedPrice);
        });
    }

    // Load places if on index page
    if (window.location.pathname.includes('index.html') || window.location.pathname === '/') {
        const token = getCookie('token');
        if (token) {
            fetchPlaces(token);
        } else {
            // Display sample places if not logged in
            displaySamplePlaces();
        }
    }

    // Load place details if viewing a specific place
    const placeId = getPlaceIdFromURL();
    if (placeId) {
        const token = getCookie('token');
        if (token) {
            fetchPlaceDetails(token, placeId);
        } else {
            window.location.href = 'login.html';
        }
    }
});

// Retrieve the value of a cookie by name
function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? match[2] : null;
}

// Update UI based on authentication status
function updateAuthUI() {
    const token = getCookie('token');
    const username = getCookie('username');
    
    const loginLink = document.getElementById('login-link');
    const logoutLink = document.getElementById('logout-link');
    const userInfo = document.getElementById('user-info');
    const addReview = document.getElementById('add-review');

    if (token) {
        // User is logged in
        if (loginLink) loginLink.style.display = 'none';
        if (logoutLink) logoutLink.style.display = 'inline-block';
        if (userInfo) {
            userInfo.textContent = `Hello, ${username || 'User'}`;
            userInfo.style.display = 'inline-block';
        }
        if (addReview) addReview.style.display = 'block';
    } else {
        // User is not logged in
        if (loginLink) loginLink.style.display = 'inline-block';
        if (logoutLink) logoutLink.style.display = 'none';
        if (userInfo) userInfo.style.display = 'none';
        if (addReview) addReview.style.display = 'none';
    }
}

// Send login request to the API and store token if successful
async function loginUser(email, password) {
    try {
        const response = await fetch('http://localhost:5000/api/v1/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            const data = await response.json();
            
            // Store token in cookies
            document.cookie = `token=${data.access_token}; path=/; Secure`;
            
            // Store username if available
            if (data.user && data.user.email) {
                document.cookie = `username=${data.user.email}; path=/; Secure`;
            }
            
            window.location.href = 'index.html';
        } else {
            const errorData = await response.json();
            const errorMessage = document.getElementById('error-message');
            if (errorMessage) {
                errorMessage.textContent = errorData.error || 'Login failed. Please check your credentials.';
                errorMessage.style.display = 'block';
            } else {
                alert('Login failed: ' + (errorData.error || 'Unknown error'));
            }
        }
    } catch (error) {
        console.error('Error during login:', error);
        const errorMessage = document.getElementById('error-message');
        if (errorMessage) {
            errorMessage.textContent = 'Connection error. Please try again.';
            errorMessage.style.display = 'block';
        } else {
            alert('An error occurred. Please try again.');
        }
    }
}

// Logout user by removing cookies
function logoutUser() {
    document.cookie = 'token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT';
    document.cookie = 'username=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT';
    window.location.href = 'index.html';
}

// Fetch list of all places from the API
async function fetchPlaces(token) {
    try {
        const response = await fetch('http://localhost:5000/api/v1/places', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
        } else {
            console.error('Failed to fetch places data');
            displaySamplePlaces();
        }
    } catch (error) {
        console.error('Error fetching places:', error);
        displaySamplePlaces();
    }
}

// Display sample places when not logged in or if API fails
function displaySamplePlaces() {
    const placesContainer = document.getElementById('places-container');
    if (!placesContainer) return;

    placesContainer.innerHTML = `
        <div class="place-card">
            <h2>Beautiful Beach House</h2>
            <p>Price per night: $150</p>
            <button class="view-details-btn" onclick="redirectToLogin()">View Details</button>
        </div>
        
        <div class="place-card">
            <h2>Cozy Cabin</h2>
            <p>Price per night: $100</p>
            <button class="view-details-btn" onclick="redirectToLogin()">View Details</button>
        </div>

        <div class="place-card">
            <h2>Modern Apartment</h2>
            <p>Price per night: $200</p>
            <button class="view-details-btn" onclick="redirectToLogin()">View Details</button>
        </div>
    `;
}

// Redirect to login page when a non-logged in user tries to view details
function redirectToLogin() {
    window.location.href = 'login.html';
}

// Render list of places in the DOM
function displayPlaces(places) {
    const placesContainer = document.getElementById('places-container');
    if (!placesContainer) return;
    
    placesContainer.innerHTML = '';

    if (places.length === 0) {
        placesContainer.innerHTML = '<p>No places available</p>';
        return;
    }

    places.forEach(place => {
        const placeCard = document.createElement('div');
        placeCard.classList.add('place-card');
        placeCard.innerHTML = `
            <h2>${place.name || place.title || 'No title available'}</h2>
            <p>Price per night: $${place.price || 'N/A'}</p>
            <button class="view-details-btn" onclick="window.location.href='place.html?id=${place.id}'">View Details</button>
        `;
        placesContainer.appendChild(placeCard);
    });
}

// Filter displayed places based on selected price
function filterPlacesByPrice(selectedPrice) {
    const placesContainer = document.getElementById('places-container');
    if (!placesContainer) return;
    
    const placeCards = Array.from(placesContainer.getElementsByClassName('place-card'));

    placeCards.forEach(place => {
        const priceText = place.querySelector('p').textContent;
        const price = parseInt(priceText.replace('Price per night: $', '').trim());

        if (selectedPrice === 'All' || price <= parseInt(selectedPrice)) {
            place.style.display = 'block';
        } else {
            place.style.display = 'none';
        }
    });
}

// Extract place ID from URL query parameters
function getPlaceIdFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('id');
}

// Fetch detailed information about a specific place
async function fetchPlaceDetails(token, placeId) {
    try {
        const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const placeDetails = await response.json();
            displayPlaceDetails(placeDetails);
        } else {
            console.error('Failed to fetch place details');
        }
    } catch (error) {
        console.error('Error fetching place details:', error);
    }
}

// Display detailed view of a single place, including reviews
function displayPlaceDetails(place) {
    const placeDetailsContainer = document.getElementById('place-details');
    if (!placeDetailsContainer) return;

    placeDetailsContainer.innerHTML = `
        <h1 id="place-title">${place.name || place.title || 'No title available'}</h1>
        <div class="place-details">
            <p><strong>Price:</strong> $${place.price || 'N/A'}</p>
            <p><strong>Description:</strong> ${place.description || 'No description available'}</p>
            <p><strong>Amenities:</strong> ${place.amenities ? (Array.isArray(place.amenities) ? 
                place.amenities.map(a => a.name).join(', ') : place.amenities.name) : 'No amenities listed'}</p>
        </div>
        <h2>Reviews</h2>
        <div id="reviews">
            ${place.reviews && place.reviews.length > 0 ? 
                place.reviews.map(review => `
                    <div class="review-card">
                        <p><strong>Rating:</strong> ${review.rating}/5</p>
                        <p>${review.text}</p>
                    </div>
                `).join('') : 
                '<p>No reviews yet</p>'}
        </div>
    `;

    // Show review form if user is authenticated
    const addReviewSection = document.getElementById('add-review');
    if (addReviewSection) {
        addReviewSection.innerHTML = `
            <h3>Add a Review</h3>
            <form id="review-form">
                <div class="form-group">
                    <label for="rating">Rating (1-5)</label>
                    <select id="rating" name="rating" required>
                        <option value="5">5 - Excellent</option>
                        <option value="4">4 - Good</option>
                        <option value="3">3 - Average</option>
                        <option value="2">2 - Poor</option>
                        <option value="1">1 - Very Poor</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="comment">Comment</label>
                    <textarea id="comment" name="comment" required></textarea>
                </div>
                <button type="submit" class="login-button">Submit Review</button>
            </form>
        `;

        // Submit new review on form submission
        const reviewForm = document.getElementById('review-form');
        if (reviewForm) {
            reviewForm.addEventListener('submit', (event) => {
                event.preventDefault();
                const rating = document.getElementById('rating').value;
                const comment = document.getElementById('comment').value;
                submitReview(place.id, rating, comment);
            });
        }
    }
}

// Function to submit a new review
async function submitReview(placeId, rating, comment) {
    const token = getCookie('token');
    if (!token) {
        window.location.href = 'login.html';
        return;
    }
    
    try {
        const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}/reviews`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ rating, 'text': comment })
        });

        if (response.ok) {
            alert('Review added successfully!');
            document.getElementById('review-form').reset();
            window.location.reload();
        } else {
            const errorData = await response.json();
            alert('Review failed: ' + (errorData.error || 'Unknown error'));
        } 
    } catch (error) {
        console.error('Error submitting review:', error);
        alert('An error occurred. Please try again.');
    }
}