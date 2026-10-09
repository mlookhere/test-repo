import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PageElements(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[tuple[str, dict[str, str | None]]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.append((tag, dict(attrs)))


class LayoutTests(unittest.TestCase):
    page: PageElements
    css: str

    @classmethod
    def setUpClass(cls) -> None:
        cls.page = PageElements()
        cls.page.feed((ROOT / "index.html").read_text(encoding="utf-8"))
        cls.css = (ROOT / "assets/styles.css").read_text(encoding="utf-8")

    def test_page_has_landmarks_and_headings(self) -> None:
        names = [tag for tag, _ in self.page.tags]
        for landmark in ("header", "nav", "main", "footer", "h1", "h2", "h3"):
            self.assertIn(landmark, names)
        self.assertEqual(names.count("h1"), 1)
        self.assertEqual(names.count("article"), 3)
        self.assertTrue(any(tag == "nav" and attrs.get("aria-label") for tag, attrs in self.page.tags))

    def test_navigation_and_skip_link_targets_exist(self) -> None:
        ids = {attrs["id"] for _, attrs in self.page.tags if "id" in attrs}
        anchors = [
            attrs.get("href")
            for tag, attrs in self.page.tags
            if tag == "a" and (attrs.get("href") or "").startswith("#")
        ]
        self.assertIn("#main", anchors)
        self.assertIn("#features", anchors)
        self.assertIn("#about", anchors)
        for href in anchors:
            self.assertIn(str(href)[1:], ids, f"Missing target for {href}")

    def test_responsive_layout_and_keyboard_focus(self) -> None:
        self.assertIn("grid-template-columns: repeat(3, minmax(0, 1fr))", self.css)
        self.assertIn("@media (max-width: 700px)", self.css)
        self.assertIn("grid-template-columns: 1fr", self.css)
        self.assertIn("a:focus-visible", self.css)
        self.assertIn(".skip-link:focus", self.css)
        self.assertIn("prefers-reduced-motion: reduce", self.css)


if __name__ == "__main__":
    unittest.main()
