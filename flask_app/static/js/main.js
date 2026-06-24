/* ===== Ivan Soriano Photography — Main JS ===== */

// ---- Smooth scroll ----
function smoothScroll(selector) {
  var el = document.querySelector(selector);
  if (el) el.scrollIntoView({ behavior: "smooth" });
}

// ---- Navbar scroll state ----
(function () {
  var navbar = document.getElementById("navbar");
  if (!navbar) return;
  function onScroll() {
    navbar.style.backgroundColor = "rgba(8,12,9,0.92)";
    navbar.style.backdropFilter = "blur(16px)";
    navbar.style.borderBottom = "1px solid rgba(200,169,110,0.12)";
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
})();

// ---- Mobile menu ----
var mobileMenu = null;
var menuIconContainer = null;

function toggleMobileMenu() {
  mobileMenu = document.getElementById("mobile-menu");
  menuIconContainer = document.getElementById("mobile-menu-btn");
  if (mobileMenu.style.display === "none" || !mobileMenu.style.display) {
    mobileMenu.style.display = "flex";
    mobileMenu.classList.add("mobile-menu-open");
    menuIconContainer.innerHTML = '<i data-lucide="x" id="menu-icon" style="width: 26px; height: 26px;"></i>';
  } else {
    closeMobileMenu();
  }
  lucide.createIcons();
}

function closeMobileMenu() {
  mobileMenu = document.getElementById("mobile-menu");
  menuIconContainer = document.getElementById("mobile-menu-btn");
  if (mobileMenu && mobileMenu.style.display !== "none") {
    mobileMenu.classList.remove("mobile-menu-open");
    mobileMenu.classList.add("mobile-menu-close");
    setTimeout(function () {
      mobileMenu.style.display = "none";
      mobileMenu.classList.remove("mobile-menu-close");
    }, 350);
  }
  if (menuIconContainer) {
    menuIconContainer.innerHTML = '<i data-lucide="menu" id="menu-icon" style="width: 26px; height: 26px;"></i>';
    lucide.createIcons();
  }
}

// ---- Scroll reveal (IntersectionObserver) ----
(function () {
  var observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("revealed");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1, rootMargin: "0px 0px -60px 0px" }
  );

  document.querySelectorAll(".reveal, .reveal-x-left, .reveal-x-right, .reveal-scale").forEach(function (el) {
    observer.observe(el);
  });
})();

// ---- Portfolio filter ----
function filterPortfolio(category, btn) {
  var items = document.querySelectorAll(".portfolio-item");
  var buttons = document.querySelectorAll(".portfolio-filter");

  buttons.forEach(function (b) {
    b.classList.remove("active");
    b.style.color = "var(--isp-text-muted)";
    b.style.backgroundColor = "transparent";
    b.style.borderColor = "rgba(122,140,126,0.3)";
  });

  btn.classList.add("active");
  btn.style.color = "var(--isp-bg)";
  btn.style.backgroundColor = "var(--isp-gold)";
  btn.style.borderColor = "var(--isp-gold)";

  items.forEach(function (item) {
    var cat = item.getAttribute("data-category");
    if (category === "All" || cat === category) {
      item.style.display = "";
      item.classList.remove("hide");
    } else {
      item.classList.add("hide");
      setTimeout(function () {
        if (item.classList.contains("hide")) {
          item.style.display = "none";
        }
      }, 300);
    }
  });
}

// ---- Lightbox ----
function openLightbox(src, alt, title, location) {
  var lightbox = document.getElementById("lightbox");
  var img = document.getElementById("lightbox-img");
  var titleEl = document.getElementById("lightbox-title");
  var locationEl = document.getElementById("lightbox-location");

  img.src = src;
  img.alt = alt;
  titleEl.textContent = title;
  locationEl.textContent = location;

  lightbox.style.display = "flex";
  document.body.style.overflow = "hidden";
}

function closeLightbox() {
  var lightbox = document.getElementById("lightbox");
  var content = document.getElementById("lightbox-content");

  content.classList.add("closing");
  lightbox.classList.add("closing");

  setTimeout(function () {
    lightbox.style.display = "none";
    lightbox.classList.remove("closing");
    content.classList.remove("closing");
    document.body.style.overflow = "";
  }, 300);
}

// Click overlay to close
(function () {
  var lightbox = document.getElementById("lightbox");
  if (lightbox) {
    lightbox.addEventListener("click", function (e) {
      if (e.target === lightbox) closeLightbox();
    });
  }
  var closeBtn = document.getElementById("lightbox-close");
  if (closeBtn) {
    closeBtn.addEventListener("click", closeLightbox);
  }
})();

// Portfolio item click -> open lightbox
(function () {
  document.querySelectorAll(".portfolio-item").forEach(function (item) {
    item.addEventListener("click", function () {
      var src = item.getAttribute("data-src");
      var alt = item.getAttribute("data-alt");
      var title = item.getAttribute("data-title");
      var location = item.getAttribute("data-location");
      openLightbox(src, alt, title, location);
    });
  });
})();

// ---- Toast (replacing sonner) ----
function showToast(message) {
  var container = document.getElementById("toast-container");
  var toast = document.createElement("div");
  toast.className = "toast";
  toast.style.cssText =
    "background-color: var(--isp-bg-card); border: 1px solid rgba(200,169,110,0.3); color: var(--isp-cream); padding: 16px 24px; font-family: var(--font-body); font-size: 14px; border-radius: 4px; max-width: 360px; box-shadow: 0 8px 24px rgba(0,0,0,0.4);";
  toast.textContent = message;
  container.appendChild(toast);

  setTimeout(function () {
    toast.classList.add("closing");
    setTimeout(function () {
      if (toast.parentNode) toast.parentNode.removeChild(toast);
    }, 300);
  }, 4000);
}

// ---- Contact form ----
(function () {
  var form = document.getElementById("contact-form");
  if (!form) return;

  var submitBtn = document.getElementById("cf-submit");

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    // Clear previous errors
    form.querySelectorAll(".form-input").forEach(function (input) {
      input.classList.remove("error");
    });

    var name = form.querySelector("#cf-name").value.trim();
    var email = form.querySelector("#cf-email").value.trim();
    var phone = form.querySelector("#cf-phone").value.trim();
    var eventType = form.querySelector("#cf-event-type").value;
    var eventDate = form.querySelector("#cf-event-date").value;
    var message = form.querySelector("#cf-message").value.trim();

    var hasErrors = false;

    if (!name) {
      form.querySelector("#cf-name").classList.add("error");
      hasErrors = true;
    }
    if (!email || !/^\S+@\S+$/.test(email)) {
      form.querySelector("#cf-email").classList.add("error");
      hasErrors = true;
    }
    if (!eventType) {
      form.querySelector("#cf-event-type").classList.add("error");
      hasErrors = true;
    }
    if (!message) {
      form.querySelector("#cf-message").classList.add("error");
      hasErrors = true;
    }

    if (hasErrors) return;

    submitBtn.disabled = true;
    submitBtn.textContent = "Sending...";
    submitBtn.style.cursor = "not-allowed";
    submitBtn.style.backgroundColor = "var(--isp-green-dark)";

    fetch("/api/contact", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: name,
        email: email,
        phone: phone,
        eventType: eventType,
        eventDate: eventDate,
        message: message,
      }),
    })
      .then(function (res) { return res.json(); })
      .then(function (data) {
        if (data.success) {
          showToast(data.message || "Message sent! Ivan will be in touch soon.");
          form.reset();
        } else {
          showToast("Something went wrong. Please try again.");
        }
      })
      .catch(function () {
        showToast("Network error. Please try again.");
      })
      .finally(function () {
        submitBtn.disabled = false;
        submitBtn.textContent = "Send Inquiry";
        submitBtn.style.cursor = "pointer";
        submitBtn.style.backgroundColor = "var(--isp-green)";
      });
  });
})();

// ---- Footer year ----
(function () {
  var yearEl = document.getElementById("current-year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();
})();

// ---- Back to top button ----
(function () {
  var btn = document.getElementById("back-to-top");
  if (!btn) return;

  function onScroll() {
    if (window.scrollY > 400) {
      btn.style.opacity = "1";
      btn.style.visibility = "visible";
    } else {
      btn.style.opacity = "0";
      btn.style.visibility = "hidden";
    }
  }

  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  btn.addEventListener("click", function () {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
})();

// ---- Escape key to close lightbox ----
document.addEventListener("keydown", function (e) {
  if (e.key === "Escape") {
    var lightbox = document.getElementById("lightbox");
    if (lightbox && lightbox.style.display !== "none") {
      closeLightbox();
    }
  }
});
