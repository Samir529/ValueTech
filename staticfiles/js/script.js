// function openNav() {
//   document.getElementById("mySidenav").style.width = "250px";
// }
//
// function closeNav() {
//   document.getElementById("mySidenav").style.width = "0";
// }

function toggleNav() {
  const menu = document.getElementById("sidenavjs");
  if (menu.style.width === "250px") {
    menu.style.width = "0";
  } else {
    menu.style.width = "250px";
  }
}

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