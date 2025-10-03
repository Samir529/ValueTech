// Wrap everything in an IIFE to avoid global variables
(function() {

    // ======= COMMON BACK-TO-TOP BUTTON =======
    // Back-to-Top Button
    // Configuration
    document.addEventListener("DOMContentLoaded", () => {
    const SHOW_AFTER_Y = 200; // px scrolled before showing the button

    const backToTopDesktop = document.getElementById('backToTop');
    const backToTopMobile = document.getElementById("mobileBackToTop");

    function handleBackToTop(btn) {
      if (btn) {
        window.addEventListener("scroll", () => {
          if (window.scrollY > SHOW_AFTER_Y) {
            btn.classList.add("show");
          } else {
            btn.classList.remove("show");
          }
        });

        // Click -> smooth scroll to top
        btn.addEventListener("click", () => {
          window.scrollTo({ top: 0, behavior: "smooth" });
        });
      }
  }
  handleBackToTop(backToTopDesktop);
  handleBackToTop(backToTopMobile);
});


    // ======= SIDENAV TOGGLE =======
    // Side Navigation Menu
    window.toggleNav = function () {
      const menu = document.getElementById("sidenavjs");

      if (menu.style.width === "260px") {
        menu.style.width = "0";
        menu.removeEventListener("mouseenter", blockPageScroll);
        menu.removeEventListener("mouseleave", allowPageScroll);
        allowPageScroll(); // Ensure page scroll is restored
      } else {
        menu.style.width = "260px";
        menu.addEventListener("mouseenter", blockPageScroll);
        menu.addEventListener("mouseleave", allowPageScroll);
        blockPageScroll();
      }
    };

    function blockPageScroll() {
      window.addEventListener("wheel", preventPageScroll, { passive: false });
      window.addEventListener("touchmove", preventPageScroll, { passive: false });
    }

    function allowPageScroll() {
      window.removeEventListener("wheel", preventPageScroll, { passive: false });
      window.removeEventListener("touchmove", preventPageScroll, { passive: false });
    }

    function preventPageScroll(e) {
      const sidenav = document.getElementById("sidenavjs");

      if (sidenav.contains(e.target)) {
        // Inside sidenav, check if scroll should be blocked
        const atTop = sidenav.scrollTop === 0 && e.deltaY < 0;
        const atBottom =
          sidenav.scrollHeight - sidenav.scrollTop === sidenav.clientHeight &&
          e.deltaY > 0;

        if (atTop || atBottom) {
          e.preventDefault();
        }
        return; // allow scroll inside sidenav if not hitting limit
      }

      // Outside sidenav: block scroll when sidenav is open
      e.preventDefault();
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


    // ======= TOOLTIP ACTIVATION =======
    // Activate all tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(el => new bootstrap.Tooltip(el, {
        trigger: 'hover focus'   // ensures tooltip hides on mouse leave or focus out
    }));


    // ======= STICKY NAVBAR & CATEGORY BAR =======
    // Make Navbar and Category bar sticky
    window.addEventListener("scroll", function () {
        const navbar = document.querySelector(".navbar");
        const topbar = document.querySelector(".topbar");
        const categoryBar = document.querySelector(".category-bar");
        const topbarHeight = topbar ? topbar.offsetHeight : 0;

        if (window.scrollY >= topbarHeight) {
            navbar?.classList.add("sticky");
            categoryBar?.classList.add("sticky");
            document.body.style.paddingTop = navbar?.offsetHeight + 'px';
        } else {
            navbar?.classList.remove("sticky");
            categoryBar?.classList.remove("sticky");
            document.body.style.paddingTop = '0';
        }
    });


    // ================= Live Search Dropdown / AJAX live results =================
    (function () {
      const searchInput = document.getElementById("search-input");
      if (!searchInput) return;

      const form = searchInput.closest("form") || document;
      const resultsBox = form.querySelector("#search-results") || document.getElementById("search-results");
      if (!resultsBox) return;

      // Disable browser autofill/autocomplete
      try {
        form.setAttribute("autocomplete", "off");
        searchInput.setAttribute("autocomplete", "new-password");
        searchInput.setAttribute("autocorrect", "off");
        searchInput.setAttribute("autocapitalize", "off");
        searchInput.setAttribute("spellcheck", "false");
      } catch (e) { }

      let activeTab = "product";
      let debounceTimer = null;

      function hideResults() {
        resultsBox.style.display = "none";
        resultsBox.innerHTML = "";
        resultsBox.dataset.open = "0";
      }

      function renderTabContent(products, categories, tab) {
        const items = (tab === "product") ? products : categories;
        if (!items.length) return `<div class="search-no-result">No ${tab} found</div>`;

        return items.map(item => {
          let displayName = item.name;

          // Remove "Category:" prefix if it's a category
          if (item.type === "category") {
            displayName = displayName.replace(/^Category:\s*/i, "");
          }

          // Format prices with comma
          function formatPrice(p) {
            return Number(p).toLocaleString("en-US");
          }

          let priceHtml = "";
          if (item.special_price) {
            // Show special price and strike-through regular price
            priceHtml = `
              <span class="result-price ms-1">
                ${formatPrice(item.special_price)}৳
                <small class="text-muted" style="text-decoration: line-through; margin-left:5px;">
                  ${formatPrice(item.regular_price)}৳
                </small>
              </span>
            `;
          } else if (item.regular_price) {
            priceHtml = `<span class="result-price ms-1">${formatPrice(item.regular_price)}৳</span>`;
          }

          return `
            <a href="${item.url}" class="search-result-item ${item.type}" role="option">
              <img src="${item.image || '/static/assets/images/Default images/no-image-available-icon-vector.jpg'}" class="result-img" alt="">
              <div class="result-details">
                <span class="result-name ms-1">${displayName}</span>
                ${priceHtml}
              </div>
            </a>
          `;
        }).join("");
      }

      function buildDropdown(products, categories, query) {
        const tabsHtml = `
          <div class="search-results-tabs">
            <button type="button" class="${activeTab === 'product' ? 'active' : ''}" data-tab="product">
              Products (${products.length})
            </button>
            <button type="button" class="${activeTab === 'category' ? 'active' : ''}" data-tab="category">
              Categories (${categories.length})
            </button>
          </div>
        `;

        const contentHtml = `
          <div class="search-results-content">
            ${renderTabContent(products, categories, activeTab)}
            <div class="search-see-all">
              <a href="/store/search/?search_field=${encodeURIComponent(query)}">
                <button class="button2 w-100 mb-1" style="border-radius: 3px; border: none;">
                    <span>See all results</span>
                </button>
              </a>
            </div>
          </div>
        `;

        resultsBox.innerHTML = tabsHtml + contentHtml;
        resultsBox.dataset.open = "1";
        resultsBox.style.display = "block";

        const tabButtons = resultsBox.querySelectorAll(".search-results-tabs button");

        tabButtons.forEach(btn => {
          btn.addEventListener("click", function (e) {
            e.preventDefault();
            activeTab = this.dataset.tab;
            tabButtons.forEach(b => b.classList.remove("active"));
            this.classList.add("active");

            const content = resultsBox.querySelector(".search-results-content");
            if (content) {
              content.innerHTML = renderTabContent(products, categories, activeTab) + `
                <div class="search-see-all">
                  <a href="/store/search/?search_field=${encodeURIComponent(query)}">
                    <button class="button2 w-100 mb-1" style="border-radius: 3px; border: none;">
                        <span>See all results</span>
                    </button>
                  </a>
                </div>
              `;
            }
          });
        });
      }

      // Use search_field instead of q
      const endpointBase = "/store/ajax/search/?search_field=";

      async function doSearch(query) {
        try {
          const res = await fetch(`${endpointBase}${encodeURIComponent(query)}`, { credentials: "same-origin" });
          if (!res.ok) { hideResults(); return; }

          const data = await res.json();
          const products = (data.results || []).filter(i => i.type === "product");
          const categories = (data.results || []).filter(i => i.type === "category");

          if ((products.length + categories.length) === 0) {
            resultsBox.innerHTML = `<div class="search-no-result">No results found</div>`;
            resultsBox.style.display = "block";
            resultsBox.dataset.open = "1";
            return;
          }

          buildDropdown(products, categories, query); // <- pass query
        } catch (err) {
          console.error("Search error:", err);
          hideResults();
        }
      }

      searchInput.addEventListener("input", function () {
        const query = this.value.trim();
        clearTimeout(debounceTimer);
        if (!query) {
          hideResults();
          return;
        }
        debounceTimer = setTimeout(() => doSearch(query), 180);
      });

      searchInput.addEventListener("keydown", function (e) {
        if (e.key === "Enter" && resultsBox.dataset.open === "1") {
          e.preventDefault();
          return false;
        }
      });

      resultsBox.addEventListener("click", function (e) {
        e.stopPropagation();
      });

      document.addEventListener("click", function (e) {
        if (!form.contains(e.target)) hideResults();
      });

    })();


    // Cart Panel
    window.openCart = function (e) {
      e.preventDefault();
      document.getElementById("cartPanel").classList.add("open");
    };

    window.closeCart = function () {
      document.getElementById("cartPanel").classList.remove("open");
    };




    // ======= MOBILE-SPECIFIC BEHAVIOR =======
    function initMobileFeatures() {
        // Only apply if viewport <= 768px (adjust if needed)
        if (window.innerWidth > 768) return;


        // Mobile Search Toggle
        document.querySelector(".mobile-search-button").addEventListener("click", function () {
            document.querySelector(".mobile-search-box").classList.toggle("show");
        });

        // Adjust Mobile Search Box When Navbar Shrinks in Sticky Mode
        (function () {
          const mobileBox = document.getElementById('mobileSearchBox');
          const navbar = document.querySelector('.navbar');

          if (!mobileBox || !navbar) return;

          function updateMobileSearchTop() {
            // use the current navbar height so it works for sticky / non-sticky and responsive
            const topValue = navbar.offsetHeight || 0;
            mobileBox.style.top = `${topValue}px`;
          }

          // run at important times
          document.addEventListener('DOMContentLoaded', updateMobileSearchTop);
          window.addEventListener('resize', updateMobileSearchTop);
          window.addEventListener('scroll', updateMobileSearchTop);

          // If you have custom code that toggles .navbar.sticky, call updateMobileSearchTop() right after toggling.
          // e.g. inside your scroll handler, after navbar.classList.add/remove('sticky'), call updateMobileSearchTop();
        })();


        // ================= Live Search Dropdown For Mobile / AJAX live results =================
        (function () {
          const searchBoxes = [
            { input: document.getElementById("search-input"), results: document.getElementById("search-results") },   // desktop
            { input: document.getElementById("mobile-search-input"), results: document.getElementById("mobile-search-results") } // mobile
          ];

          searchBoxes.forEach(({ input, results }) => {
            if (!input || !results) return;

            const form = input.closest("form") || document;
            let activeTab = "product";
            let debounceTimer = null;

            function hideResults() {
              results.style.display = "none";
              results.innerHTML = "";
              results.dataset.open = "0";
            }

            function renderTabContent(products, categories, tab) {
              const items = (tab === "product") ? products : categories;
              if (!items.length) return `<div class="search-no-result">No ${tab} found</div>`;

              return items.map(item => {
                let displayName = item.name;
                if (item.type === "category") displayName = displayName.replace(/^Category:\s*/i, "");

                function formatPrice(p) {
                  return Number(p).toLocaleString("en-US");
                }

                let priceHtml = "";
                if (item.special_price) {
                  priceHtml = `
                    <span class="result-price ms-1">
                      ${formatPrice(item.special_price)}৳
                      <small class="text-muted" style="text-decoration: line-through; margin-left:5px;">
                        ${formatPrice(item.regular_price)}৳
                      </small>
                    </span>
                  `;
                } else if (item.regular_price) {
                  priceHtml = `<span class="result-price ms-1">${formatPrice(item.regular_price)}৳</span>`;
                }

                return `
                  <a href="${item.url}" class="search-result-item ${item.type}" role="option">
                    <img src="${item.image || '/static/assets/images/Default images/no-image-available-icon-vector.jpg'}" class="result-img" alt="">
                    <div class="result-details">
                      <span class="result-name ms-1">${displayName}</span>
                      ${priceHtml}
                    </div>
                  </a>
                `;
              }).join("");
            }

            function buildDropdown(products, categories, query) {
              const tabsHtml = `
                <div class="search-results-tabs">
                  <button type="button" class="${activeTab === 'product' ? 'active' : ''}" data-tab="product">
                    Products (${products.length})
                  </button>
                  <button type="button" class="${activeTab === 'category' ? 'active' : ''}" data-tab="category">
                    Categories (${categories.length})
                  </button>
                </div>
              `;

              const contentHtml = `
                <div class="search-results-content">
                  ${renderTabContent(products, categories, activeTab)}
                  <div class="search-see-all">
                    <a href="/store/search/?search_field=${encodeURIComponent(query)}">
                      <button class="button2 w-100 mb-1" style="border-radius: 3px; border: none;">
                          <span>See all results</span>
                      </button>
                    </a>
                  </div>
                </div>
              `;

              results.innerHTML = tabsHtml + contentHtml;
              results.dataset.open = "1";
              results.style.display = "block";

              const tabButtons = results.querySelectorAll(".search-results-tabs button");
              tabButtons.forEach(btn => {
                btn.addEventListener("click", function (e) {
                  e.preventDefault();
                  activeTab = this.dataset.tab;
                  tabButtons.forEach(b => b.classList.remove("active"));
                  this.classList.add("active");

                  const content = results.querySelector(".search-results-content");
                  if (content) {
                    content.innerHTML = renderTabContent(products, categories, activeTab) + `
                      <div class="search-see-all">
                        <a href="/store/search/?search_field=${encodeURIComponent(query)}">
                          <button class="button2 w-100 mb-1" style="border-radius: 3px; border: none;">
                              <span>See all results</span>
                          </button>
                        </a>
                      </div>
                    `;
                  }
                });
              });
            }

            const endpointBase = "/store/ajax/search/?search_field=";

            async function doSearch(query) {
              try {
                const res = await fetch(`${endpointBase}${encodeURIComponent(query)}`, { credentials: "same-origin" });
                if (!res.ok) { hideResults(); return; }

                const data = await res.json();
                const products = (data.results || []).filter(i => i.type === "product");
                const categories = (data.results || []).filter(i => i.type === "category");

                if ((products.length + categories.length) === 0) {
                  results.innerHTML = `<div class="search-no-result">No results found</div>`;
                  results.style.display = "block";
                  results.dataset.open = "1";
                  return;
                }

                buildDropdown(products, categories, query);
              } catch (err) {
                console.error("Search error:", err);
                hideResults();
              }
            }

            input.addEventListener("input", function () {
              const query = this.value.trim();
              clearTimeout(debounceTimer);
              if (!query) {
                hideResults();
                return;
              }
              debounceTimer = setTimeout(() => doSearch(query), 180);
            });

            input.addEventListener("keydown", function (e) {
              if (e.key === "Enter" && results.dataset.open === "1") {
                e.preventDefault();
                return false;
              }
            });

            results.addEventListener("click", function (e) {
              e.stopPropagation();
            });

            document.addEventListener("click", function (e) {
              if (!form.contains(e.target)) hideResults();
            });

          }); // end forEach
        })();


        // Side Dropdown Category Menu
        (function() {
  document.addEventListener("DOMContentLoaded", function () {
    const menu = document.getElementById("sideCategoryMenu");
    const overlay = document.getElementById("overlay");
    const openBtn = document.querySelector(".category-toggle");
    const closeBtn = document.querySelector(".close-btn");

    if (!menu || !overlay || !openBtn || !closeBtn) return;

    openBtn.addEventListener("click", function () {
      menu.classList.add("open");
      overlay.classList.add("show");
    });

    closeBtn.addEventListener("click", function () {
      menu.classList.remove("open");
      overlay.classList.remove("show");
    });

    overlay.addEventListener("click", function () {
      menu.classList.remove("open");
      overlay.classList.remove("show");
    });

    document.querySelectorAll("[data-toggle]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        const target = document.getElementById(this.dataset.toggle);
        target.classList.toggle("open");
      });
    });
  });
})();


    }


    // Run on page load
    document.addEventListener("DOMContentLoaded", initMobileFeatures);


    // Optional: handle window resize to re-initialize mobile features
    window.addEventListener("resize", initMobileFeatures);

})();
