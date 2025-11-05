// Mobile menu toggle script
const toggleButton = document.querySelector('.menu-toggle');
const navMenu = document.getElementById('nav-menu');

toggleButton.addEventListener('click', () => {
  const expanded = toggleButton.getAttribute('aria-expanded') === 'true';
  // Toggle the aria-expanded state
  toggleButton.setAttribute('aria-expanded', String(!expanded));
  // Toggle the menu visibility class
  navMenu.classList.toggle('open', !expanded);
});

// Optional: close the menu when a link is clicked (for one-page navigation)
navMenu.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => {
    if (window.innerWidth < 600) {
      navMenu.classList.remove('open');
      toggleButton.setAttribute('aria-expanded', 'false');
    }
  });
});
