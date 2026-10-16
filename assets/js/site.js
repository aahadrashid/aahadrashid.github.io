(function () {
  "use strict";

  const menuButton = document.querySelector("[data-menu-toggle]");
  const navigation = document.querySelector("[data-navigation]");
  const menuLabel = document.querySelector("[data-menu-label]");

  if (menuButton && navigation) {
    const closeMenu = () => {
      menuButton.setAttribute("aria-expanded", "false");
      menuButton.setAttribute("aria-label", "Open navigation");
      if (menuLabel) menuLabel.textContent = "Menu";
      navigation.classList.remove("is-open");
    };

    menuButton.addEventListener("click", () => {
      const isOpen = menuButton.getAttribute("aria-expanded") === "true";
      menuButton.setAttribute("aria-expanded", String(!isOpen));
      menuButton.setAttribute("aria-label", isOpen ? "Open navigation" : "Close navigation");
      if (menuLabel) menuLabel.textContent = isOpen ? "Menu" : "Close";
      navigation.classList.toggle("is-open", !isOpen);
    });
    navigation.addEventListener("click", (event) => {
      if (event.target.closest("a")) closeMenu();
    });
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") closeMenu();
    });
    document.addEventListener("click", (event) => {
      if (!navigation.contains(event.target) && !menuButton.contains(event.target)) closeMenu();
    });
  }

  const search = document.querySelector("[data-project-search]");
  const categorySelect = document.querySelector("[data-filter-select]");
  const cards = Array.from(document.querySelectorAll("[data-project-card]"));
  const resultCount = document.querySelector("[data-results-count]");
  const noResults = document.querySelector("[data-no-results]");
  let activeFilter = "all";

  if (search && cards.length) {
    const updateResults = () => {
      const query = search.value.trim().toLocaleLowerCase();
      let visible = 0;

      for (const card of cards) {
        const matchesCategory = activeFilter === "all" || card.dataset.category === activeFilter;
        const matchesSearch = !query || (card.dataset.search || "").includes(query);
        const show = matchesCategory && matchesSearch;
        card.hidden = !show;
        if (show) visible += 1;
      }

      if (resultCount) resultCount.textContent = `${visible} ${visible === 1 ? "project" : "projects"} shown`;
      if (noResults) noResults.hidden = visible !== 0;
    };

    search.addEventListener("input", updateResults);
    if (categorySelect) {
      categorySelect.addEventListener("change", () => {
        activeFilter = categorySelect.value;
        updateResults();
      });
    }
    updateResults();
  }

})();
