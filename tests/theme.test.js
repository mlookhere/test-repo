import assert from "node:assert/strict";
import test from "node:test";

import { mountThemeToggle } from "../assets/app.js";

function page() {
  const handlers = new Map();
  const button = {
    hidden: true,
    attrs: new Map(),
    setAttribute(name, value) {
      this.attrs.set(name, value);
    },
    addEventListener(name, fn) {
      handlers.set(name, fn);
    },
  };
  const root = {
    documentElement: { dataset: {} },
    querySelector: () => button,
  };
  return { root, button, click: () => handlers.get("click")() };
}

test("respects initial system dark preference and keyboard-native button semantics", () => {
  const fixture = page();
  assert.equal(mountThemeToggle({ root: fixture.root, prefersDark: true }), true);
  assert.equal(fixture.root.documentElement.dataset.theme, "dark");
  assert.equal(fixture.button.attrs.get("aria-pressed"), "true");
  assert.equal(fixture.button.hidden, false);
});

test("saved selection wins over system preference and click persists the next theme", () => {
  const fixture = page();
  const saved = new Map([["test-site-theme", "light"]]);
  const storage = {
    getItem: (key) => saved.get(key),
    setItem: (key, value) => saved.set(key, value),
  };

  mountThemeToggle({ root: fixture.root, storage, prefersDark: true });
  assert.equal(fixture.root.documentElement.dataset.theme, "light");
  assert.equal(fixture.button.attrs.get("aria-pressed"), "false");

  fixture.click();
  assert.equal(saved.get("test-site-theme"), "dark");
  assert.equal(fixture.root.documentElement.dataset.theme, "dark");
  assert.equal(fixture.button.attrs.get("aria-pressed"), "true");
});

test("storage failures do not prevent operation", () => {
  const fixture = page();
  const storage = {
    getItem() {
      throw new Error("not available");
    },
    setItem() {
      throw new Error("not available");
    },
  };

  assert.equal(mountThemeToggle({ root: fixture.root, storage }), true);
  fixture.click();
  assert.equal(fixture.root.documentElement.dataset.theme, "dark");
});

test("does nothing when the toggle is absent", () => {
  assert.equal(mountThemeToggle({ root: { querySelector: () => null } }), false);
});
