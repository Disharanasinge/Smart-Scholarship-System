// Smart Scholarship Verification System
// Frontend Script — Handles star rating, alerts, delete confirmation, search, nav highlight, character counter
// Author: Disha J | BCA Final Year Project 2025-26

document.addEventListener("DOMContentLoaded", function () {

  // Star Rating 
  const stars = document.querySelectorAll(".star");
  const ratingInput = document.getElementById("ratingInput");

  stars.forEach(function (star, index) {
    star.addEventListener("click", function () {
      const val = index + 1;
      if (ratingInput) ratingInput.value = val;
      stars.forEach(function (s, i) {
        s.classList.toggle("filled", i < val);
      });
    });

    star.addEventListener("mouseover", function () {
      stars.forEach(function (s, i) {
        s.classList.toggle("filled", i <= index);
      });
    });

    star.addEventListener("mouseout", function () {
      const currentVal = ratingInput ? parseInt(ratingInput.value) : 0;
      stars.forEach(function (s, i) {
        s.classList.toggle("filled", i < currentVal);
      });
    });
  });

  // Pre-fill stars if user already rated 
  if (ratingInput && ratingInput.value) {
    const val = parseInt(ratingInput.value);
    stars.forEach(function (s, i) {
      s.classList.toggle("filled", i < val);
    });
  }

  // Auto-dismiss alerts 
  const alerts = document.querySelectorAll(".alert");
  alerts.forEach(function (alert) {
    setTimeout(function () {
      alert.style.transition = "opacity 0.5s";
      alert.style.opacity = "0";
      setTimeout(function () { alert.remove(); }, 500);
    }, 3500);
  });

  // Confirm delete 
  const deleteForms = document.querySelectorAll(".delete-form");
  deleteForms.forEach(function (form) {
    form.addEventListener("submit", function (e) {
      if (!confirm("Are you sure you want to delete this scholarship? This action cannot be undone and will remove it for all students.")) {
        e.preventDefault();
      }
    });
  });

  // Hero search redirect 
  const heroSearchForm = document.getElementById("heroSearchForm");
  if (heroSearchForm) {
    heroSearchForm.addEventListener("submit", function (e) {
      e.preventDefault();
      const q = document.getElementById("heroSearchInput").value.trim();
      if (q) {
        window.location.href = "/student/home?search=" + encodeURIComponent(q);
      }
    });
  }

  // Active nav link highlight 
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll(".sidebar .nav-link");
  navLinks.forEach(function (link) {
    if (link.getAttribute("href") === currentPath) {
      link.classList.add("active");
    }
  });

  // Textarea character counter 
  const textareas = document.querySelectorAll("textarea");
  textareas.forEach(function (ta) {
    ta.addEventListener("input", function () {
      const max = 500;
      const remaining = max - ta.value.length;
      let counter = ta.nextElementSibling;
      if (!counter || !counter.classList.contains("char-counter")) {
        counter = document.createElement("small");
        counter.classList.add("char-counter", "text-muted");
        ta.parentNode.insertBefore(counter, ta.nextSibling);
      }
      counter.innerText = remaining + " characters remaining";
      if (remaining < 50) {
        counter.style.color = "var(--risky)";
      } else {
        counter.style.color = "";
      }
    });
  });

  // Scroll to top on page load
  window.scrollTo(0, 0);

}); // END of DOMContentLoaded 