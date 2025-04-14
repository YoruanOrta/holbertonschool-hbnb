// Handles authentication, place display/filtering, details, and reviews.
document.addEventListener('DOMContentLoaded', () => {
    // Check authentication and update the UI
    updateAuthUI();
    
    // Set up login form if on the login page
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            loginUser();
        });
    }
    
    // If we are on the main page, display sample places and set up the filter
    if (window.location.pathname.endsWith('index.html') || window.location.pathname === '/') {
        displaySamplePlaces();
        
        const priceFilter = document.getElementById('price-filter');
        if (priceFilter) {
            priceFilter.addEventListener('change', function() {
                filterPlacesByPrice(this.value);
            });
        }
    }
    
    // If we are on the place details page, load the data
    if (window.location.pathname.includes('place.html')) {
        const placeId = getPlaceIdFromURL();
        if (placeId) {
            fetchPlaceDetails(placeId);
            setupReviewForm();
        }
    }
    
    // Set up logout button
    const logoutLink = document.getElementById('logout-link');
    if (logoutLink) {
        logoutLink.addEventListener('click', function(e) {
            e.preventDefault();
            logoutUser();
        });
    }
});

// Function to display sample places
function displaySamplePlaces() {
    const placesContainer = document.getElementById('places-container');
    if (!placesContainer) return;

    placesContainer.innerHTML = `
        <div class="place-card">
            <h2>Beautiful Beach House</h2>
            <p>Price per night: $150</p>
            <button class="view-details-btn" data-id="1">View Details</button>
        </div>
        
        <div class="place-card">
            <h2>Cozy Cabin</h2>
            <p>Price per night: $100</p>
            <button class="view-details-btn" data-id="2">View Details</button>
        </div>

        <div class="place-card">
            <h2>Modern Apartment</h2>
            <p>Price per night: $200</p>
            <button class="view-details-btn" data-id="3">View Details</button>
        </div>
    `;
    
    // Set up the "View Details" buttons after creating the cards
    setupViewDetailsButtons();
}

// Function to set up "View Details" buttons
function setupViewDetailsButtons() {
    const viewDetailsButtons = document.querySelectorAll('.view-details-btn');
    
    viewDetailsButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Get the place ID from the data-id attribute
            const placeId = this.getAttribute('data-id');
            
            // Redirect to the details page (without checking authentication)
            window.location.href = `place.html?id=${placeId}`;
        });
    });
}

// Function to update the UI based on authentication state
function updateAuthUI() {
    const token = localStorage.getItem('token');
    const userData = JSON.parse(localStorage.getItem('userData') || '{}');
    
    const loginLink = document.getElementById('login-link');
    const logoutLink = document.getElementById('logout-link');
    const userInfo = document.getElementById('user-info');
    
    if (token) {
        // Authenticated user
        if (loginLink) loginLink.style.display = 'none';
        if (logoutLink) logoutLink.style.display = 'inline-block';
        if (userInfo) {
            userInfo.style.display = 'inline-block';
            userInfo.textContent = userData.email || 'Usuario';
        }
    } else {
        // Unauthenticated user
        if (loginLink) loginLink.style.display = 'inline-block';
        if (logoutLink) logoutLink.style.display = 'none';
        if (userInfo) userInfo.style.display = 'none';
    }
}

// Function to log in
function loginUser() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    fetch('http://localhost:5000/api/v1/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Login failed');
        }
        return response.json();
    })
    .then(data => {
        // Save token and user data
        localStorage.setItem('token', data.token);
        localStorage.setItem('userData', JSON.stringify({
            id: data.user_id,
            email: email
        }));
        
        // Redirect to the main page
        window.location.href = 'index.html';
    })
    .catch(error => {
        console.error('Error during login:', error);
        alert('Login failed. Please check your credentials and try again.');
    });
}

// Function to log out
function logoutUser() {
    // Remove token and user data
    localStorage.removeItem('token');
    localStorage.removeItem('userData');
    
    // Update the UI
    updateAuthUI();

    window.location.reload();
}

// Function to filter places by price
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

// Function to get the place ID from the URL
function getPlaceIdFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('id');
}

// Function to fetch the place details
function fetchPlaceDetails(placeId) {
    const samplePlaceData = {
        1: {
            id: 1,
            name: "Beautiful Beach House",
            price_per_night: 150,
            user_name: "John Doe",
            description: "A beautiful beach house with amazing views...",
            amenities: [
                { name: "WiFi" },
                { name: "Pool" },
                { name: "Air Conditioning" }
            ],
            reviews: [
                { user_name: "Jane Smith", text: "Great place to stay!", rating: 4 },
                { user_name: "Robert Brown", text: "Amazing location and very comfortable.", rating: 5 }
            ]
        },
        2: {
            id: 2,
            name: "Cozy Cabin",
            price_per_night: 100,
            user_name: "Sarah Johnson",
            description: "A comfortable cabin in the woods perfect for a weekend getaway.",
            amenities: [
                { name: "Fireplace" },
                { name: "WiFi" },
                { name: "Kitchen" }
            ],
            reviews: [
                { user_name: "Michael Davis", text: "Very peaceful and relaxing.", rating: 5 },
                { user_name: "Emily White", text: "Lovely cabin, would stay again!", rating: 4 }
            ]
        },
        3: {
            id: 3,
            name: "Modern Apartment",
            price_per_night: 200,
            user_name: "David Wilson",
            description: "A sleek modern apartment in the heart of downtown.",
            amenities: [
                { name: "WiFi" },
                { name: "Gym" },
                { name: "Parking" }
            ],
            reviews: [
                { user_name: "Thomas Lee", text: "Great location and amenities.", rating: 5 },
                { user_name: "Laura Chen", text: "Very clean and comfortable.", rating: 4 }
            ]
        }
    };

    // Simulate an API call
    setTimeout(() => {
        if (samplePlaceData[placeId]) {
            displayPlaceDetails(samplePlaceData[placeId]);
        } else {
            console.error(`Place with ID ${placeId} not found`);
            alert('Place not found. Returning to home page...');
            window.location.href = 'index.html';
        }
    }, 500);
}

// Function to display place details
function displayPlaceDetails(placeData) {
    document.title = placeData.name || 'Place Details';
    
    // Update the main title
    const placeTitle = document.querySelector('.place-title');
    if (placeTitle) {
        placeTitle.textContent = placeData.name;
    }
    
    // Update place details
    const placeDetails = document.getElementById('place-details');
    if (placeDetails) {
        placeDetails.innerHTML = `
            <div class="detail-card">
                <p><strong>Host:</strong> ${placeData.user_name || 'Unknown'}</p>
                <p><strong>Price per night:</strong> $${placeData.price_per_night}</p>
                <p><strong>Description:</strong> ${placeData.description || 'No description available'}</p>
                <div class="amenities">
                    <p><strong>Amenities:</strong> ${displayAmenities(placeData.amenities)}</p>
                </div>
            </div>
        `;
    }
    
    // Display reviews
    displayReviews(placeData.reviews || []);
}

// Function to display amenities
function displayAmenities(amenities) {
    if (!amenities || amenities.length === 0) {
        return 'No amenities listed';
    }
    
    return amenities.map(amenity => amenity.name).join(', ');
}

// Function to display reviews
function displayReviews(reviews) {
    const reviewsSection = document.getElementById('reviews-section');
    if (!reviewsSection) return;
    
    const reviewsList = document.getElementById('reviews-list');
    if (!reviewsList) return;
    
    if (reviews.length === 0) {
        reviewsList.innerHTML = '<p>No reviews yet.</p>';
        return;
    }
    
    reviewsList.innerHTML = '';
    
    reviews.forEach(review => {
        const reviewElement = document.createElement('div');
        reviewElement.className = 'review-card';
        reviewElement.innerHTML = `
            <p><strong>${review.user_name || 'Anonymous'}</strong></p>
            <p>${review.text}</p>
            <p class="rating">Rating: ${displayStars(review.rating)}</p>
        `;
        reviewsList.appendChild(reviewElement);
    });
}

// Function to display rating stars
function displayStars(rating) {
    const fullStar = '★';
    const emptyStar = '☆';
    let stars = '';
    
    for (let i = 1; i <= 5; i++) {
        if (i <= rating) {
            stars += fullStar;
        } else {
            stars += emptyStar;
        }
    }
    
    return stars;
}

// Function to set up the review form
function setupReviewForm() {
    const token = localStorage.getItem('token');
    const reviewFormSection = document.getElementById('add-review-section');
    
    if (!reviewFormSection) return;
    
    if (!token) {
        // Unauthenticated user, display message
        reviewFormSection.innerHTML = `
            <p>Please <a href="login.html">login</a> to add a review.</p>
        `;
        return;
    }
    
    // Authenticated user, display form
    reviewFormSection.innerHTML = `
        <h2>Add a Review</h2>
        <form id="review-form">
            <div class="form-group">
                <label for="rating">Rating:</label>
                    <select id="rating" required>
                    <option value="1">1 ★</option>
                    <option value="2">2 ★★</option>
                    <option value="3">3 ★★★</option>
                    <option value="4">4 ★★★★</option>
                    <option value="5">5 ★★★★★</option>
                </select>
            </div>
            <div class="form-group">
                <label for="review-text">Your Review:</label>
                <textarea id="review-text" rows="4" required></textarea>
            </div>
            <button type="submit" class="submit-review-btn">Submit Review</button>
        </form>
    `;
    
    // Set up the form submission event
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', submitReview);
    }
}

// Function to submit a review
function submitReview(e) {
    e.preventDefault();
    
    const placeId = getPlaceIdFromURL();
    const token = localStorage.getItem('token');
    const reviewText = document.getElementById('review-text').value;
    const rating = document.getElementById('rating').value;
    
    if (!token) {
        alert('You must be logged in to submit a review.');
        return;
    }

    alert('Review submitted successfully! (Demo mode)');
    
    // Simulate a new review
    const userData = JSON.parse(localStorage.getItem('userData') || '{}');
    const reviewsList = document.getElementById('reviews-list');
    
    if (reviewsList) {
        const newReview = document.createElement('div');
        newReview.className = 'review-card';
        newReview.innerHTML = `
            <p><strong>${userData.email || 'You'}</strong></p>
            <p>${reviewText}</p>
            <p class="rating">Rating: ${displayStars(parseInt(rating))}</p>
        `;
        
        // Add the new review to the beginning of the list
        reviewsList.insertBefore(newReview, reviewsList.firstChild);
    }
    
    // Clear the form
    document.getElementById('review-text').value = '';
    document.getElementById('rating').value = '5';
}