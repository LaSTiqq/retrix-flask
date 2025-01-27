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
