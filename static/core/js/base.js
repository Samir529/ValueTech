// Side Navigation Menu
function toggleNav() {
  const menu = document.getElementById("sidenavjs");
  if (menu.style.width === "250px") {
    menu.style.width = "0";
  } else {
    menu.style.width = "250px";
  }
}

// function openNav() {
//   document.getElementById("mySidenav").style.width = "250px";
// }
// function closeNav() {
//   document.getElementById("mySidenav").style.width = "0";
// }

// function toggleNav() {
//     const menu = document.getElementById("mySidenav");
//     menu.style.width = (menu.style.width === "250px") ? "0" : "250px";
// }

// function toggleNav() {
//   const menu = document.getElementById("mySidenav");
//   const currentWidth = window.getComputedStyle(menu).width;
//
//   if (currentWidth === "0px") {
//       menu.style.width = "250px";
//   } else {
//       menu.style.width = "0";
//   }
// }

// function toggleNav() {
//     const menu = document.getElementById("mySidenav");
//     const currentWidth = window.getComputedStyle(menu).width;
//     menu.style.width = (currentWidth === "0px") ? "250" : "0px";
// }


// Activate all tooltips
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(el => new bootstrap.Tooltip(el, {
  trigger: 'hover focus'   // ensures tooltip hides on mouse leave or focus out
}));


// Make Navbar and Category bar sticky
window.addEventListener("scroll", function () {
    const navbar = document.querySelector(".navbar");
    const topbar = document.querySelector(".topbar");
    const categoryBar = document.querySelector(".category-bar");
    const topbarHeight = topbar ? topbar.offsetHeight : 0;

    if (window.scrollY >= topbarHeight) {
        navbar.classList.add("sticky");
        categoryBar.classList.add("sticky");
        document.body.style.paddingTop = navbar.offsetHeight + 'px';
    } else {
        navbar.classList.remove("sticky");
        categoryBar.classList.remove("sticky");
        document.body.style.paddingTop = '0';
    }
});


// Back-to-Top Button
// Configuration
const SHOW_AFTER_Y = 200; // px scrolled before showing the button

const btn = document.getElementById('backToTop');
let raf = null;

// Show/hide on scroll with rAF for performance
window.addEventListener('scroll', () => {
    if (raf) return;
    raf = requestAnimationFrame(() => {
    if (window.scrollY > SHOW_AFTER_Y) {
    btn.classList.add('show');
    } else {
    btn.classList.remove('show');
    }
    raf = null;
    });
    }, { passive: true });

// Click -> smooth scroll to top
btn.addEventListener('click', (e) => {
    e.preventDefault();
    window.scrollTo({ top: 0, behavior: 'smooth' });
});
