document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;

    // ===== INDEX: SHOW PLACES =====
    if (path.includes('index.html') || path === '/' || path.endsWith('/')) {
        const placesContainer = document.querySelector('#places-container');

        if (placesContainer) {
            const places = [
                { id: 1, name: 'Cozy Cabin', price: 80 },
                { id: 2, name: 'Beach House', price: 120 },
                { id: 3, name: 'Mountain Retreat', price: 100 }
            ];

            places.forEach(place => {
                const card = document.createElement('div');
                card.className = 'place-card';
                card.innerHTML = `
                    <h3>${place.name}</h3>
                    <p>Price per night: $${place.price}</p>
                    <button class="details-button" onclick="viewPlace(${place.id})">View Details</button>
                `;
                placesContainer.appendChild(card);
            });
        }

        // Change login to logout
        const loginLink = document.querySelector('#login-link');
        const user = localStorage.getItem('user');
        if (loginLink && user) {
            loginLink.textContent = 'Logout';
            loginLink.href = '#';
            loginLink.addEventListener('click', () => {
                localStorage.removeItem('user');
                window.location.reload();
            });
        }
    }
    // ===== PLACE DETAILS =====
    else if (path.includes('place.html')) {
        const urlParams = new URLSearchParams(window.location.search);
        const placeId = urlParams.get('id');
        if (path.includes('place.html')) {
            const params = new URLSearchParams(window.location.search);
            const placeId = params.get('id');
        
            fetchPlaceDetails(placeId);
            fetchPlaceReviews(placeId);
        
            const user = localStorage.getItem('user');
            if (user) {
                const reviewAction = document.getElementById('review-action');
                reviewAction.innerHTML = `
                <a href="add_review.html?id=${placeId}" class="add-review-button">Add Review</a>
                `;
            }
            }
        }

    // ===== ADD REVIEW PAGE =====
    else if (path.includes('add_review.html')) {
        const form = document.querySelector('#review-form');
        const urlParams = new URLSearchParams(window.location.search);
        const placeId = urlParams.get('id');

        const select = document.querySelector('#rating');
        if (select) {
            for (let i = 1; i <= 5; i++) {
                const option = document.createElement('option');
                option.value = i;
                option.textContent = i;
                select.appendChild(option);
            }
        }

        if (form) {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                const reviewText = form.review.value;
                const rating = form.rating.value;
                const user = localStorage.getItem('user') || 'Guest';

                console.log('Review Submitted:', {
                    placeId,
                    review: reviewText,
                    rating,
                    user
                });

                window.location.href = `place.html?id=${placeId}`;
            });
        }
    }
    // ===== LOGIN PAGE =====
    else if (path.includes('login.html')) {
        const loginForm = document.querySelector('#login-form');

        if (loginForm) {
            loginForm.addEventListener('submit', (e) => {
                e.preventDefault();
                const username = loginForm.username.value;
                localStorage.setItem('user', username);
                alert(`Logged in as ${username}`);
                window.location.href = 'index.html';
            });
        }
    }
});

function fetchPlaceDetails(placeId) {
    const placesList = document.getElementById('places-list');
    fetch(`/api/v1/places/${placeId}`)
        .then(response => response.json())
        .then(place => {
            document.getElementById('Place').textContent = place.name;
            document.title = `${place.name} - Hbnb`;

        const html = `
            <div class="info-row"><strong>Price:</strong> $${place.price_per_night}</div>
            <div class="info-row"><strong>Description:</strong> ${place.description}</div>
        `;
    document.getElementById('place-info').innerHTML = html;
    })
    .catch(error => {
        console.error('Error loading place details:', error);
    });
}

function fetchPlaceReviews(placeId) {
    fetch(`/api/v1/places/${placeId}/reviews`)
        .then(response => response.json())
        .then(reviews => {
            const reviewsList = document.getElementById('reviews-list');
            let html = '';

            reviews.forEach(review => {
            const stars = '★'.repeat(review.rating) + '☆'.repeat(5 - review.rating);
            html += `
                <div class="review-card">
                    <div class="reviewer-name">${review.user || 'Anonymous'}</div>
                    <div class="review-text">${review.text}</div>
                    <div class="review-rating">${stars}</div>
                </div>
            `;
        });

        reviewsList.innerHTML = html;
    })
    .catch(error => {
        console.error('Error loading reviews:', error);
    });
}