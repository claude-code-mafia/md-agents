// Main JavaScript for md agents documentation

document.addEventListener('DOMContentLoaded', function() {
  // Mobile menu toggle
  const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
  const sidebar = document.querySelector('.sidebar');
  const sidebarClose = document.querySelector('.sidebar-close');
  let overlay = null;

  // Create overlay element
  function createOverlay() {
    overlay = document.createElement('div');
    overlay.className = 'sidebar-overlay';
    document.body.appendChild(overlay);
    
    overlay.addEventListener('click', closeSidebar);
  }

  // Open sidebar
  function openSidebar() {
    if (!overlay) createOverlay();
    sidebar.classList.add('active');
    mobileMenuToggle.classList.add('active');
    overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  // Close sidebar
  function closeSidebar() {
    sidebar.classList.remove('active');
    mobileMenuToggle.classList.remove('active');
    if (overlay) overlay.classList.remove('active');
    document.body.style.overflow = '';
  }

  // Toggle sidebar
  if (mobileMenuToggle) {
    mobileMenuToggle.addEventListener('click', function() {
      if (sidebar.classList.contains('active')) {
        closeSidebar();
      } else {
        openSidebar();
      }
    });
  }

  // Close button
  if (sidebarClose) {
    sidebarClose.addEventListener('click', closeSidebar);
  }

  // Close sidebar when clicking on a link (mobile)
  document.querySelectorAll('.sidebar-nav a').forEach(link => {
    link.addEventListener('click', function() {
      if (window.innerWidth < 1024) {
        closeSidebar();
      }
    });
  });

  // Handle desktop menu toggle for home page
  if (window.innerWidth >= 1024 && sidebar && sidebar.classList.contains('sidebar-hidden')) {
    const desktopToggle = document.createElement('button');
    desktopToggle.className = 'desktop-menu-toggle';
    desktopToggle.innerHTML = '<i class="fas fa-bars"></i> Menu';
    desktopToggle.style.cssText = 'position: fixed; left: 1rem; top: 80px; z-index: 100; padding: 0.5rem 1rem; background: var(--primary); color: white; border: none; border-radius: 4px; cursor: pointer;';
    document.body.appendChild(desktopToggle);

    desktopToggle.addEventListener('click', function() {
      sidebar.classList.toggle('active');
      this.innerHTML = sidebar.classList.contains('active') ? '<i class="fas fa-times"></i> Close' : '<i class="fas fa-bars"></i> Menu';
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
    // Create copy button
    const copyBtn = document.createElement('button');
    copyBtn.className = 'copy-btn';
    copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
    copyBtn.style.cssText = 'position: absolute; top: 0.5rem; right: 0.5rem; padding: 0.25rem 0.5rem; background: var(--secondary); color: white; border: none; border-radius: 3px; cursor: pointer; opacity: 0; transition: opacity 0.3s;';
    
    // Make pre position relative for absolute button
    block.style.position = 'relative';
    block.appendChild(copyBtn);
    
    // Show button on hover
    block.addEventListener('mouseenter', () => copyBtn.style.opacity = '1');
    block.addEventListener('mouseleave', () => copyBtn.style.opacity = '0');
    
    copyBtn.addEventListener('click', function(e) {
      e.stopPropagation();
      const code = block.textContent.replace('', ''); // Remove copy icon
      navigator.clipboard.writeText(code).then(() => {
        copyBtn.innerHTML = '<i class="fas fa-check"></i>';
        setTimeout(() => {
          copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
        }, 2000);
      });
    });
  });
});