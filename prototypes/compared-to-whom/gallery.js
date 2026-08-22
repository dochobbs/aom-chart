(() => {
  const preview = document.querySelector("#concept-preview");
  const stage = document.querySelector(".preview-stage");
  const openCurrent = document.querySelector("#open-current");
  const address = document.querySelector(".browser-chrome span");
  let concept = "restrained";

  const loadConcept = (next) => {
    concept = next;
    const href = `article.html?concept=${concept}`;
    preview.src = href;
    openCurrent.href = href;
    address.textContent = `compared-to-whom / ${concept}`;
    document.querySelectorAll("[data-concept]").forEach((button) => {
      button.setAttribute("aria-pressed", String(button.dataset.concept === concept));
    });
  };

  document.querySelectorAll("button[data-concept]").forEach((button) => {
    button.addEventListener("click", () => loadConcept(button.dataset.concept));
  });

  document.querySelectorAll("button[data-viewport]").forEach((button) => {
    button.addEventListener("click", () => {
      stage.dataset.viewport = button.dataset.viewport;
      document.querySelectorAll("button[data-viewport]").forEach((candidate) => {
        candidate.setAttribute("aria-pressed", String(candidate === button));
      });
    });
  });
})();
