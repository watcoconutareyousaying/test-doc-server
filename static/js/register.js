async function registerUser(event) {
  event.preventDefault();

  const formData = new FormData(event.target);
  const data = Object.fromEntries(formData.entries());

  try {
    const response = await fetch(apiRegisterUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (response.ok) {
      const result = await response.json();
      alert("Registration successful!");
      window.location.href = "/account/login/";
    } else {
      const error = await response.json();
      alert("Registration failed: " + JSON.stringify(error));
    }
  } catch (err) {
    console.error("Error:", err);
    alert("An error occurred during registration.");
  }
}
