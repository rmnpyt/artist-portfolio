document.addEventListener("DOMContentLoaded", function () {
    const navToggle = document.getElementById("nav-toggle");
    const navMenu = document.getElementById("nav-menu");

    navToggle.addEventListener("click", function () {
      navMenu.classList.toggle("open");
    });

    // Mobile submenu toggle (click on parent link)
    const submenuParents = document.querySelectorAll(".has-submenu > a");

    submenuParents.forEach(function (link) {
      link.addEventListener("click", function (e) {
        const isMobile = window.matchMedia("(max-width: 768px)").matches;
        if (isMobile) {
          e.preventDefault();
          const parentLi = this.parentElement;
          parentLi.classList.toggle("submenu-open");
        }
      });
    });

    // Image protection - prevent right-click, drag, and saving
    // Disable right-click context menu on all images
    document.addEventListener("contextmenu", function (e) {
      if (e.target.tagName === "IMG") {
        e.preventDefault();
        return false;
      }
    });

    // Prevent drag-and-drop on all images
    document.addEventListener("dragstart", function (e) {
      if (e.target.tagName === "IMG") {
        e.preventDefault();
        return false;
      }
    });

    // Disable specific keyboard shortcuts for saving images
    document.addEventListener("keydown", function (e) {
      // Prevent Ctrl+S (Save)
      if ((e.ctrlKey || e.metaKey) && e.key === "s") {
        e.preventDefault();
        return false;
      }
    });
  });