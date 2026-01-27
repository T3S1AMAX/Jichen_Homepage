document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".abstract, .bibtex").forEach((el) => {
    el.classList.remove("open");
    el.style.height = "0px";
    el.style.overflow = "hidden";
    el.addEventListener("transitionend", (event) => {
      if (event.propertyName !== "height") return;
      if (el.classList.contains("open")) {
        el.style.height = "auto";
      }
    });
  });

  document.addEventListener("click", (event) => {
    const link = event.target.closest("a[data-toggle]");
    if (!link) return;
    event.preventDefault();
    toggleDisplay(link.dataset.toggle);
  });
});

function toggleDisplay(elementId) {
  const el = document.getElementById(elementId);
  if (!el) return;
  const isOpen = el.classList.contains("open");

  if (isOpen) {
    // Collapse with animation
    if (el.style.height === "auto") {
      el.style.height = el.scrollHeight + "px";
    }
    requestAnimationFrame(() => {
      el.classList.remove("open");
      el.style.height = "0px";
    });
    return;
  }

  // Expand with animation
  el.classList.add("open");
  el.style.height = "0px";
  requestAnimationFrame(() => {
    el.style.height = el.scrollHeight + "px";
  });
}

function toggleAbstract(pubId) {
  toggleDisplay("abs-" + pubId);
}

function toggleBibtex(pubId) {
  toggleDisplay("bib-" + pubId);
}
