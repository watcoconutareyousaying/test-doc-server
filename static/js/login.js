async function loginUser(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = {
        email: formData.get("email"),
        password: formData.get("password"),
    };

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const response = await fetch(apiLoginUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify(data),
    });

    if (response.ok) {
        const result = await response.json();
        alert("Login successful!");
        localStorage.setItem("access_token", result.access);
        localStorage.setItem("refresh_token", result.refresh)
        window.location.href = "/";
    } else {
        alert("Login failed. Check your email or password.");
    }
}