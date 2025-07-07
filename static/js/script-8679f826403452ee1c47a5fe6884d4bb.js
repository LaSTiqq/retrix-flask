// Resize logo onscroll
const logo = document.getElementById("logo");

const scrollFunction = () => {
  const scrolled =
    document.body.scrollTop > 50 || document.documentElement.scrollTop > 50;

  const setLogoSize = (logo, width, height) => {
    if (logo) {
      logo.style.width = width;
      logo.style.height = height;
    }
  };

  if (scrolled) {
    setLogoSize(logo, "130px", "66px");
  } else {
    setLogoSize(logo, "158px", "80px");
  }
};

window.onscroll = () => {
  scrollFunction();
};

// Hide navbar after click when navbar collapsed
const navbarLinks = document.querySelectorAll(".navbar-collapse a");

navbarLinks.forEach((link) => {
  link.addEventListener("click", () => {
    const navbarCollapse = document.querySelector(".navbar-collapse");
    if (navbarCollapse.classList.contains("show")) {
      navbarCollapse.classList.remove("show");
    }
  });
});

// AJAX form submission
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("form");
  const loader = document.getElementById("loader");

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    loader.classList.remove("d-none");

    grecaptcha.ready(function () {
      grecaptcha
        .execute("6LdceGonAAAAANTvW5D13lPX4Ac8pNVo_X0MLdUc", {
          action: "contact",
        })
        .then(async function (token) {
          document.getElementById("g-recaptcha-response").value = token;

          const formData = new FormData(form);
          try {
            const response = await fetch("/send-ajax", {
              method: "POST",
              headers: {
                "X-CSRFToken": formData.get("csrf_token"),
              },
              body: formData,
            });

            const result = await response.json();
            showAlert(result.message, result.status);

            if (result.status !== "info") {
              form.reset();
            }
          } catch (err) {
            showAlert("Something went wrong! Please try again.", "danger");
          } finally {
            loader.classList.add("d-none");
          }
        });
    });
  });

  const showAlert = (message, type) => {
    const alert = document.getElementById("alert");

    alert.className = `alert alert-${type} alert-dismissible rounded-pill fw-bold d-block`;
    alert.innerHTML = `
      ${message}
      <button type="button" class="btn-close" aria-label="Close"></button>
  `;

    const closeButton = alert.querySelector(".btn-close");
    if (closeButton) {
      closeButton.addEventListener("click", () => {
        alert.classList.add("d-none");
        alert.className = "alert d-none";
      });
    }

    setTimeout(() => {
      alert.classList.add("d-none");
      alert.className = "alert d-none";
    }, 4000);
  };
});
