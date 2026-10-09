import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ElementCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.elements: list[tuple[str, dict[str, str | None]]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.elements.append((tag, dict(attrs)))


class SiteTests(unittest.TestCase):
    markup: str
    elements: list[tuple[str, dict[str, str | None]]]

    @classmethod
    def setUpClass(cls) -> None:
        cls.markup = (ROOT / "index.html").read_text(encoding="utf-8")
        collector = ElementCollector()
        collector.feed(cls.markup)
        cls.elements = collector.elements

    def test_document_is_accessible_and_responsive(self) -> None:
        self.assertTrue(self.markup.lstrip().lower().startswith("<!doctype html>"))
        self.assertIn(("html", {"lang": "en"}), self.elements)
        self.assertTrue(any(tag == "main" for tag, _ in self.elements))
        self.assertTrue(
            any(tag == "meta" and attrs.get("name") == "viewport" for tag, attrs in self.elements)
        )

    def test_greeting_is_available_without_javascript(self) -> None:
        self.assertIn("Hello, world!", self.markup)
        self.assertTrue(any("data-greeting" in attrs for _, attrs in self.elements))

    def test_local_assets_exist(self) -> None:
        stylesheet = [
            attrs.get("href")
            for tag, attrs in self.elements
            if tag == "link" and attrs.get("rel") == "stylesheet"
        ]
        scripts = [attrs.get("src") for tag, attrs in self.elements if tag == "script"]
        self.assertIn("./assets/styles.css", stylesheet)
        self.assertIn("./assets/app.js", scripts)
        for asset in stylesheet + scripts:
            self.assertTrue((ROOT / str(asset)).is_file(), f"Missing asset: {asset}")


if __name__ == "__main__":
    unittest.main()
