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
        const placeDetails = document.querySelector('#place-details');
        const reviewsContainer = document.querySelector('#reviews');

        if (placeId && placeDetails) {
            const place = {
                id: placeId,
                name: 'Cozy Cabin',
                host: 'Alice',
                price: 80,
                description: 'A cozy cabin in the woods',
                amenities: ['WiFi', 'Fireplace', 'Kitchen']
            };

            placeDetails.innerHTML = `
                <div class="place-details">
                    <div class="place-info">
                        <h1>${place.name}</h1>
                        <p><strong>Host:</strong> ${place.host}</p>
                        <p><strong>Price:</strong> $${place.price}/night</p>
                        <p><strong>Description:</strong> ${place.description}</p>
                        <p><strong>Amenities:</strong> ${place.amenities.join(', ')}</p>
                    </div>
                </div>
            `;

            const reviews = [
                { user: 'John', comment: 'Great place!', rating: 5 },
                { user: 'Emma', comment: 'Really cozy and clean.', rating: 4 }
            ];

            reviews.forEach(review => {
                const div = document.createElement('div');
                div.className = 'review-card';
                div.innerHTML = `
                    <div class="username">${review.user}</div>
                    <div class="rating">Rating: ${review.rating}/5</div>
                    <p>${review.comment}</p>
                `;
                reviewsContainer.appendChild(div);
            });

            const isLoggedIn = localStorage.getItem('user');
            if (isLoggedIn) {
                const addReviewBtn = document.createElement('a');
                addReviewBtn.href = `add_review.html?id=${placeId}`;
                addReviewBtn.textContent = 'Add a Review';
                addReviewBtn.className = 'details-button';
                document.querySelector('#add-review-btn').appendChild(addReviewBtn);
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

// Redirects from the "View Details" button"
function viewPlace(id) {
    window.location.href = `place.html?id=${id}`;
}