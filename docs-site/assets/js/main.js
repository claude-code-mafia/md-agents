// Main JavaScript for md agents documentation

// Add active class to current navigation item
document.addEventListener('DOMContentLoaded', function() {
  // Mobile menu toggle (if needed in future)
  const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
  if (mobileMenuToggle) {
    mobileMenuToggle.addEventListener('click', function() {
      document.querySelector('.sidebar').classList.toggle('active');
    });
  }

  // Smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });

  // Copy code blocks on click
  document.querySelectorAll('pre').forEach(block => {
    block.addEventListener('click', function() {
      const code = this.innerText;
      navigator.clipboard.writeText(code).then(() => {
        // Visual feedback
        const originalBg = this.style.background;
        this.style.background = '#d4edda';
        setTimeout(() => {
          this.style.background = originalBg;
        }, 200);
      });
    });
  });
});