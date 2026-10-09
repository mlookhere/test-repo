export function mountGreeting(root = document) {
  const heading = root.querySelector("[data-greeting]");
  if (!heading) return false;

  heading.textContent = "Hello, world!";
  return true;
}

if (typeof document !== "undefined") mountGreeting();
