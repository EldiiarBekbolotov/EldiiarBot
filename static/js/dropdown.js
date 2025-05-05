// (c) 2025 Eldiiar Bekbolotov. Licensed under the MIT License.
class M3Select {
  constructor(container) {
    this.container = container;
    this.select = container.querySelector(".m3-select-native");
    this.field = container.querySelector(".m3-select-field");
    this.valueSpan = container.querySelector(".m3-select-value");
    this.label = container.querySelector(".m3-select-label");
    this.menu = container.querySelector(".m3-select-menu");
    this.supportingText = container.querySelector(".m3-supporting-text");
    this.options = Array.from(this.select.options);
    this.selectedValue = "";
    this.isOpen = false;

    this.init();
  }

  init() {
    this.options.forEach((option) => {
      if (option.value !== "") {
        const li = document.createElement("li");
        li.className = "m3-select-menu-item";
        li.textContent = option.text;
        li.dataset.value = option.value;
        li.setAttribute("role", "option");
        li.setAttribute("aria-selected", "false");
        li.tabIndex = -1;
        this.menu.appendChild(li);
      }
    });

    this.field.addEventListener("click", () => this.toggleMenu());
    this.field.addEventListener("keydown", (e) => this.handleKeydown(e));
    this.menu.addEventListener("click", (e) => this.handleMenuClick(e));
    this.select.addEventListener("change", () =>
      this.updateValue(this.select.value)
    );

    document.addEventListener("click", (e) => {
      if (!this.container.contains(e.target)) {
        this.closeMenu();
      }
    });

    const savedTheme =
      localStorage.getItem("selected-theme") ||
      this.select.value ||
      "theme-dark-1";
    this.updateValue(savedTheme);
    if (this.select.disabled) {
      this.field.classList.add("disabled");
    }
  }

  toggleMenu() {
    if (this.field.classList.contains("disabled")) return;
    this.isOpen = !this.isOpen;
    this.menu.classList.toggle("open", this.isOpen);
    this.field.classList.toggle("active", this.isOpen);
    this.field.setAttribute("aria-expanded", this.isOpen);
    if (this.isOpen) {
      this.menu.querySelector(".m3-select-menu-item").focus();
    } else {
      this.field.focus();
    }
  }

  closeMenu() {
    this.isOpen = false;
    this.menu.classList.remove("open");
    this.field.classList.remove("active");
    this.field.setAttribute("aria-expanded", "false");
  }

  handleMenuClick(e) {
    const item = e.target.closest(".m3-select-menu-item");
    if (item) {
      const value = item.dataset.value;
      this.updateValue(value);
      this.closeMenu();
    }
  }

  updateValue(value) {
    this.selectedValue = value;
    const selectedOption = this.options.find((opt) => opt.value === value);
    this.valueSpan.textContent =
      selectedOption && selectedOption.value !== "" ? selectedOption.text : "";
    this.field.classList.toggle("has-value", !!value && value !== "");
    this.select.value = value;

    this.menu.querySelectorAll(".m3-select-menu-item").forEach((item) => {
      const isSelected = item.dataset.value === value;
      item.classList.toggle("selected", isSelected);
      item.setAttribute("aria-selected", isSelected);
    });

    const changeEvent = new Event("change", { bubbles: true });
    this.select.dispatchEvent(changeEvent);
  }

  handleKeydown(e) {
    if (this.field.classList.contains("disabled")) return;

    switch (e.key) {
      case "Enter":
      case "Space":
        e.preventDefault();
        this.toggleMenu();
        break;
      case "ArrowDown":
      case "ArrowUp":
        e.preventDefault();
        if (!this.isOpen) {
          this.toggleMenu();
        } else {
          const items = Array.from(
            this.menu.querySelectorAll(".m3-select-menu-item")
          );
          const current = document.activeElement;
          const index = items.indexOf(current);
          const nextIndex =
            e.key === "ArrowDown"
              ? Math.min(index + 1, items.length - 1)
              : Math.max(index - 1, 0);
          items[nextIndex].focus();
        }
        break;
      case "Escape":
        this.closeMenu();
        break;
      case "Tab":
        this.closeMenu();
        break;
    }
  }
}

document.querySelectorAll(".m3-select-container").forEach((container) => {
  new M3Select(container);
});
