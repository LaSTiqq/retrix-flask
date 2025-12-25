// Resize logo onscroll
const logo = document.getElementById("logo");

const scrollFunction = () => {
  const scrolled =
    document.body.scrollTop > 50 || document.documentElement.scrollTop > 50;

  const setLogoSize = (logo, width) => {
    if (logo) {
      logo.style.width = width;
    }
  };

  if (scrolled) {
    setLogoSize(logo, "128px");
  } else {
    setLogoSize(logo, "158px");
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
  "use strict";

  const form = document.getElementById("form");
  const loader = document.getElementById("loader");
  const alertBox = document.getElementById("alert");
  const fields = form.querySelectorAll("input, textarea");

  fields.forEach((field) => {
    field.addEventListener("input", () => {
      if (!field.checkValidity()) {
        field.classList.add("is-invalid");
        field.classList.remove("is-valid");
      } else {
        field.classList.remove("is-invalid");
        field.classList.add("is-valid");
      }
    });
  });

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    event.stopPropagation();

    if (!form.checkValidity()) {
      form.classList.add("was-validated");

      const firstInvalid = form.querySelector(":invalid");
      if (firstInvalid) {
        firstInvalid.scrollIntoView({ behavior: "smooth", block: "center" });
        firstInvalid.focus({ preventScroll: true });
      }
      return;
    }

    form.classList.add("was-validated");
    loader.classList.remove("d-none");

    grecaptcha.ready(() => {
      grecaptcha
        .execute("6LdceGonAAAAANTvW5D13lPX4Ac8pNVo_X0MLdUc", {
          action: "contact",
        })
        .then(async (token) => {
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
              form.classList.remove("was-validated");
              fields.forEach((f) => f.classList.remove("is-valid", "is-invalid"));
            }
          } catch (err) {
            showAlert("Radās kļūda! Mēģiniet vēlreiz.", "danger");
          } finally {
            loader.classList.add("d-none");
          }
        });
    });
  });

  /* ▶ Alert helper */
  function showAlert(message, type) {
    alertBox.className = `alert alert-${type} alert-dismissible rounded-pill fw-bold d-block`;
    alertBox.innerHTML = `
      ${message}
      <button type="button" class="btn-close" aria-label="Close"></button>
    `;

    alertBox.querySelector(".btn-close").addEventListener("click", () => {
      alertBox.className = "alert d-none";
    });

    setTimeout(() => {
      alertBox.className = "alert d-none";
    }, 4000);
  }
});

