window.onload = async () => {
    const user = await checkAuthStatus();

    if (user) {
        document.getElementById('welcome-message').textContent = 'Welcome, ' + user.name;
        document.getElementById('nav-links').innerHTML = `
            <li><a onclick="fetchUserProfile()">Profile</a></li>
            <li><a onclick="logoutUser()">Logout</a></li>
        `;
    } else {
        document.getElementById('welcome-message').textContent = 'Please log in or register to access more features.';
        document.getElementById('nav-links').innerHTML = `
            <li><a href="{% url 'login' %}">Login</a></li>
            <li><a href="{% url 'register' %}">Register</a></li>
        `;
    }
};