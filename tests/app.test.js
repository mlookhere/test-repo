import assert from "node:assert/strict";
import test from "node:test";

import { mountGreeting } from "../assets/app.js";

test("mounts the greeting on an existing heading", () => {
  const heading = { textContent: "" };
  const root = {
    querySelector(selector) {
      assert.equal(selector, "[data-greeting]");
      return heading;
    },
  };

  assert.equal(mountGreeting(root), true);
  assert.equal(heading.textContent, "Hello, world!");
});

test("does not crash when the heading is absent", () => {
  assert.equal(mountGreeting({ querySelector: () => null }), false);
});
