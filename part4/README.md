# HBnB - Simple Web Client

## Part 4 - Simple Web Client

In this phase, you’ll focus on the front-end development of your application using **HTML5**, **CSS3**, and **JavaScript ES6**. Your task is to design and implement an interactive user interface that connects with the back-end services developed in previous parts of the project.

---

## Objectives

- Develop a user-friendly interface following provided design specifications.
- Implement client-side functionality to interact with the back-end API.
- Ensure secure and efficient data handling using JavaScript.
- Apply modern web development practices to create a dynamic web application.

---

## Learning Goals

- Understand and apply **HTML5**, **CSS3**, and **JavaScript ES6** in a real-world project.
- Learn to interact with back-end services using **AJAX/Fetch API**.
- Implement authentication mechanisms and manage user sessions.
- Use client-side scripting to enhance user experience without page reloads.

---

## Tasks Breakdown

### **1. Design**

- Complete provided HTML and CSS files to match the given design specifications.
- Create pages for:
    - **Login**
    - **List of Places**
    - **Place Details**
    - **Add Review**

---

### **2. Login**

- Implement login functionality using the back-end API.
- Store the **JWT token** returned by the API in a cookie for session management.

---

### **3. List of Places**

- Implement the main page to display a list of all places.
- Fetch places data from the API and implement client-side filtering based on country selection.
- Ensure the page redirects to the login page if the user is not authenticated.

---

### **4. Place Details**

- Implement the detailed view of a place.
- Fetch place details from the API using the place ID.
- Provide access to the **Add Review** form if the user is authenticated.

---

### **5. Add Review**

- Implement the form to add a review for a place.
- Ensure the form is accessible only to authenticated users, redirecting others to the index page.

---

## Important Note

When testing your client against your API, you may encounter a **Cross-Origin Resource Sharing (CORS)** error. To resolve this, modify your API code to allow your client to fetch data from the API. Refer to [this article](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) for a deeper understanding of CORS and how to configure your Flask API.

---

## Resources

- [HTML5 Documentation](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5)
- [CSS3 Documentation](https://developer.mozilla.org/en-US/docs/Web/CSS)
- [JavaScript ES6 Features](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
- [Responsive Web Design Basics](https://web.dev/responsive-web-design-basics/)
- [Handling Cookies in JavaScript](https://developer.mozilla.org/en-US/docs/Web/API/Document/cookie)
- [Client-Side Form Validation](https://developer.mozilla.org/en-US/docs/Learn/Forms/Form_validation)
