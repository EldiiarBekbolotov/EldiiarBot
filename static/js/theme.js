// (c) 2025 Eldiiar Bekbolotov. Licensed under the MIT License.
const themeSelector = document.getElementById("theme-selector");

function applyTheme(theme) {
  document.body.classList.remove(
    "theme-dark-1",
    "theme-dark-2",
    "theme-dark-3",
    "theme-dark-4",
    "theme-light-1",
    "theme-light-2",
    "theme-light-3",
    "theme-light-4"
  );
  document.body.classList.add(theme);
  localStorage.setItem("selected-theme", theme);
}

document.addEventListener("DOMContentLoaded", () => {
  const savedTheme = localStorage.getItem("selected-theme") || "theme-dark-1";
  applyTheme(savedTheme);
  if (themeSelector) themeSelector.value = savedTheme;
});

if (themeSelector) {
  themeSelector.addEventListener("change", (e) => {
    applyTheme(e.target.value);
  });
}
