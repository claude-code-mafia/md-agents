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
    sidebarClose.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation();
      closeSidebar();
    });
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

  // Add copy buttons to code blocks
  document.querySelectorAll('pre').forEach(block => {
    // Create copy button
    const copyBtn = document.createElement('button');
    copyBtn.className = 'copy-btn';
    copyBtn.innerHTML = '<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M10.5 1h-6A1.5 1.5 0 0 0 3 2.5v9A1.5 1.5 0 0 0 4.5 13H5v-1h-.5a.5.5 0 0 1-.5-.5v-9a.5.5 0 0 1 .5-.5h6a.5.5 0 0 1 .5.5V3h1v-.5A1.5 1.5 0 0 0 10.5 1z"/><path d="M11.5 4h-6A1.5 1.5 0 0 0 4 5.5v9A1.5 1.5 0 0 0 5.5 16h6a1.5 1.5 0 0 0 1.5-1.5v-9A1.5 1.5 0 0 0 11.5 4zm.5 10.5a.5.5 0 0 1-.5.5h-6a.5.5 0 0 1-.5-.5v-9a.5.5 0 0 1 .5-.5h6a.5.5 0 0 1 .5.5v9z"/></svg>';
    copyBtn.setAttribute('aria-label', 'Copy code');
    
    // Make pre position relative for absolute button
    block.style.position = 'relative';
    block.appendChild(copyBtn);
    
    copyBtn.addEventListener('click', function(e) {
      e.stopPropagation();
      e.preventDefault();
      
      // Get the text content without the button text
      const codeElement = block.querySelector('code') || block;
      const code = codeElement.textContent;
      
      navigator.clipboard.writeText(code).then(() => {
        copyBtn.classList.add('copied');
        copyBtn.innerHTML = '<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M13.854 3.646a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L6.5 10.293l6.646-6.647a.5.5 0 0 1 .708 0z"/></svg>';
        
        setTimeout(() => {
          copyBtn.classList.remove('copied');
          copyBtn.innerHTML = '<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M10.5 1h-6A1.5 1.5 0 0 0 3 2.5v9A1.5 1.5 0 0 0 4.5 13H5v-1h-.5a.5.5 0 0 1-.5-.5v-9a.5.5 0 0 1 .5-.5h6a.5.5 0 0 1 .5.5V3h1v-.5A1.5 1.5 0 0 0 10.5 1z"/><path d="M11.5 4h-6A1.5 1.5 0 0 0 4 5.5v9A1.5 1.5 0 0 0 5.5 16h6a1.5 1.5 0 0 0 1.5-1.5v-9A1.5 1.5 0 0 0 11.5 4zm.5 10.5a.5.5 0 0 1-.5.5h-6a.5.5 0 0 1-.5-.5v-9a.5.5 0 0 1 .5-.5h6a.5.5 0 0 1 .5.5v9z"/></svg>';
        }, 2000);
      }).catch(err => {
        console.error('Failed to copy:', err);
      });
    });
  });
});