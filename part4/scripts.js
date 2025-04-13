document.addEventListener('DOMContentLoaded', () => {
    // Verificar autenticación y actualizar la UI
    updateAuthUI();
    
    // Configurar formulario de login si está en la página login
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            loginUser();
        });
    }
    
    // Si estamos en la página principal, mostrar lugares de muestra y configurar filtro
    if (window.location.pathname.endsWith('index.html') || window.location.pathname === '/') {
        displaySamplePlaces();
        
        const priceFilter = document.getElementById('price-filter');
        if (priceFilter) {
            priceFilter.addEventListener('change', function() {
                filterPlacesByPrice(this.value);
            });
        }
    }
    
    // Si estamos en la página de detalles de un lugar, cargar los datos
    if (window.location.pathname.includes('place.html')) {
        const placeId = getPlaceIdFromURL();
        if (placeId) {
            fetchPlaceDetails(placeId);
            setupReviewForm();
        }
    }
    
    // Configurar botón de logout
    const logoutLink = document.getElementById('logout-link');
    if (logoutLink) {
        logoutLink.addEventListener('click', function(e) {
            e.preventDefault();
            logoutUser();
        });
    }
});

// Función para mostrar lugares de muestra
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
    
    // Configurar los botones de "View Details" después de crear las tarjetas
    setupViewDetailsButtons();
}

// Función para configurar los botones "View Details"
function setupViewDetailsButtons() {
    const viewDetailsButtons = document.querySelectorAll('.view-details-btn');
    
    viewDetailsButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Obtener el ID del lugar desde el atributo data-id
            const placeId = this.getAttribute('data-id');
            
            // Redirigir a la página de detalles (sin verificar autenticación)
            window.location.href = `place.html?id=${placeId}`;
        });
    });
}

// Función para actualizar la UI basada en el estado de autenticación
function updateAuthUI() {
    const token = localStorage.getItem('token');
    const userData = JSON.parse(localStorage.getItem('userData') || '{}');
    
    const loginLink = document.getElementById('login-link');
    const logoutLink = document.getElementById('logout-link');
    const userInfo = document.getElementById('user-info');
    
    if (token) {
        // Usuario autenticado
        if (loginLink) loginLink.style.display = 'none';
        if (logoutLink) logoutLink.style.display = 'inline-block';
        if (userInfo) {
            userInfo.style.display = 'inline-block';
            userInfo.textContent = userData.email || 'Usuario';
        }
    } else {
        // Usuario no autenticado
        if (loginLink) loginLink.style.display = 'inline-block';
        if (logoutLink) logoutLink.style.display = 'none';
        if (userInfo) userInfo.style.display = 'none';
    }
}

// Función para iniciar sesión
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
        // Guardar token y datos del usuario
        localStorage.setItem('token', data.token);
        localStorage.setItem('userData', JSON.stringify({
            id: data.user_id,
            email: email
        }));
        
        // Redirigir a la página principal
        window.location.href = 'index.html';
    })
    .catch(error => {
        console.error('Error during login:', error);
        alert('Login failed. Please check your credentials and try again.');
    });
}

// Función para cerrar sesión
function logoutUser() {
    // Eliminar token y datos del usuario
    localStorage.removeItem('token');
    localStorage.removeItem('userData');
    
    // Actualizar la UI
    updateAuthUI();
    
    // Opcionalmente, recargar la página para actualizar cualquier contenido protegido
    window.location.reload();
}

// Función para filtrar lugares por precio
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

// Función para obtener el ID del lugar desde la URL
function getPlaceIdFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('id');
}

// Función para obtener los detalles del lugar
function fetchPlaceDetails(placeId) {
    // Para el propósito de esta muestra, usamos datos locales
    // En producción, esto debería ser una llamada a tu API
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

    // Simular una llamada a la API
    setTimeout(() => {
        if (samplePlaceData[placeId]) {
            displayPlaceDetails(samplePlaceData[placeId]);
        } else {
            console.error(`Place with ID ${placeId} not found`);
            alert('Place not found. Returning to home page...');
            window.location.href = 'index.html';
        }
    }, 500);

    // En producción, deberías usar el siguiente código en lugar del código de simulación anterior
    /*
    const token = localStorage.getItem('token');
    const headers = {
        'Content-Type': 'application/json'
    };
    
    // Añadir token de autenticación si existe
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    fetch(`http://localhost:5000/api/v1/places/${placeId}`, {
        method: 'GET',
        headers: headers
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to fetch place details');
        }
        return response.json();
    })
    .then(data => {
        displayPlaceDetails(data);
    })
    .catch(error => {
        console.error('Error fetching place details:', error);
        alert('Failed to load place details. Please try again later.');
    });
    */
}

// Función para mostrar los detalles del lugar
function displayPlaceDetails(placeData) {
    document.title = placeData.name || 'Place Details';
    
    // Actualizar el título principal
    const placeTitle = document.querySelector('.place-title');
    if (placeTitle) {
        placeTitle.textContent = placeData.name;
    }
    
    // Actualizar detalles del lugar
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
    
    // Mostrar reseñas
    displayReviews(placeData.reviews || []);
}

// Función para mostrar amenidades
function displayAmenities(amenities) {
    if (!amenities || amenities.length === 0) {
        return 'No amenities listed';
    }
    
    return amenities.map(amenity => amenity.name).join(', ');
}

// Función para mostrar reseñas
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

// Función para mostrar estrellas de calificación
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

// Función para configurar el formulario de reseñas
function setupReviewForm() {
    const token = localStorage.getItem('token');
    const reviewFormSection = document.getElementById('add-review-section');
    
    if (!reviewFormSection) return;
    
    if (!token) {
        // Usuario no autenticado, mostrar mensaje
        reviewFormSection.innerHTML = `
            <p>Please <a href="login.html">login</a> to add a review.</p>
        `;
        return;
    }
    
    // Usuario autenticado, mostrar formulario
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
    
    // Configurar el evento de envío del formulario
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', submitReview);
    }
}

// Función para enviar una reseña
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
    
    // Para producción, descomentar y adaptar este código
    /*
    fetch(`http://localhost:5000/api/v1/places/${placeId}/reviews`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            text: reviewText,
            rating: parseInt(rating)
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to submit review');
        }
        return response.json();
    })
    .then(data => {
        alert('Review submitted successfully!');
        // Recargar la página para mostrar la nueva reseña
        location.reload();
    })
    .catch(error => {
        console.error('Error submitting review:', error);
        alert('Failed to submit review. Please try again later.');
    });
    */
    
    // Para propósitos de demostración
    alert('Review submitted successfully! (Demo mode)');
    
    // Simular una nueva reseña
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
        
        // Añadir la nueva reseña al principio de la lista
        reviewsList.insertBefore(newReview, reviewsList.firstChild);
    }
    
    // Limpiar el formulario
    document.getElementById('review-text').value = '';
    document.getElementById('rating').value = '5';
}