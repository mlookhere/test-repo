const THEME_KEY = "test-site-theme";

export function mountGreeting(root = document) {
  const heading = root.querySelector("[data-greeting]");
  if (!heading) return false;

  heading.textContent = "Hello, world!";
  return true;
}

export function mountThemeToggle({ root = document, storage, prefersDark = false } = {}) {
  const button = root.querySelector("[data-theme-toggle]");
  if (!button) return false;

  let savedTheme = null;
  try {
    savedTheme = storage?.getItem(THEME_KEY);
  } catch {
    // Browsers may block storage; theme selection must still work for this session.
  }

  let theme =
    savedTheme === "dark" || savedTheme === "light"
      ? savedTheme
      : prefersDark
        ? "dark"
        : "light";

  function render() {
    root.documentElement.dataset.theme = theme;
    button.setAttribute("aria-pressed", String(theme === "dark"));
  }

  render();
  button.hidden = false;
  button.addEventListener("click", () => {
    theme = theme === "dark" ? "light" : "dark";
    render();
    try {
      storage?.setItem(THEME_KEY, theme);
    } catch {
      // Storage is optional; keep toggling even if writes are blocked.
    }
  });
  return true;
}

if (typeof document !== "undefined") {
  mountGreeting();
  let storage;
  try {
    storage = window.localStorage;
  } catch {
    // Private browsing can deny storage access.
  }
  mountThemeToggle({
    storage,
    prefersDark: window.matchMedia?.("(prefers-color-scheme: dark)").matches ?? false,
  });
}
