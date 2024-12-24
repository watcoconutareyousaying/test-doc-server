document.addEventListener("DOMContentLoaded", updateNavigation);

async function updateNavigation() {
  const navLinks = document.getElementById("nav-links");
  const user = await checkAuthStatus();
  const currentPage = window.location.pathname;

  if (
    currentPage.includes("/account/login/") ||
    currentPage.includes("/account/register/")
  ) {
    navLinks.style.display = "none";
    return;
  }

  if (user) {
    // User is authenticated
    navLinks.innerHTML = `
                <li><a id="profile-link" href="#">Profile</a></li>
                <li><a id="logout-link" href="#">Logout</a></li>
            `;
    document
      .getElementById("profile-link")
      .addEventListener("click", fetchUserProfile);
    document
      .getElementById("logout-link")
      .addEventListener("click", logoutUser);
  } else {
    // User is not authenticated
    navLinks.innerHTML = `
                <li><a href="/account/login/">Login</a></li>
                <li><a href="/account/register/">Register</a></li>
                `;
  }
}

async function fetchUserProfile() {
  const token = localStorage.getItem("access_token");
  if (token) {
    try {
      const response = await fetch("/account/user-profile/", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });

      if (response.ok) {
        const data = await response.json();
        alert("User profile fetched successfully!");
      } else {
        alert("Error fetching user profile. Please try again.");
      }
    } catch (error) {
      console.error("Error fetching profile:", error);
    }
  } else {
    alert("You are not authenticated.");
  }
}

async function checkAuthStatus() {
  const token = localStorage.getItem("access_token");
  if (!token) {
    return null;
  }

  try {
    const response = await fetch("/account/user-profile/", {
      method: "GET",
      headers: {
        Authorization: "Bearer " + token,
      },
    });

    if (response.ok) {
      return await response.json();
    } else {
      return null;
    }
  } catch (error) {
    console.error("Error checking auth status:", error);
    return null;
  }
}

async function logoutUser() {
  const accessToken = localStorage.getItem("access_token");
  const refreshToken = localStorage.getItem("refresh_token");

  if (!accessToken || !refreshToken) {
    alert("You are not authenticated.");
    return;
  }

  try {
    const response = await fetch("/account/logout/", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${accessToken}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ refresh: refreshToken }),
    });

    if (response.ok) {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      window.location.href = "/account/login/";
    } else {
      alert("Logout failed. Please try again.");
    }
  } catch (error) {
    console.error("Error during logout:", error);
  }
}

// Automatically update navigation on page load
document.addEventListener("DOMContentLoaded", updateNavigation);
