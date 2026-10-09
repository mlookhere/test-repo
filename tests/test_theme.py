import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ToggleParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.buttons: list[dict[str, str | None]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "button":
            self.buttons.append(dict(attrs))


class ThemeTests(unittest.TestCase):
    def test_native_toggle_is_accessible_and_hidden_without_js(self) -> None:
        parser = ToggleParser()
        parser.feed((ROOT / "index.html").read_text(encoding="utf-8"))
        self.assertEqual(len(parser.buttons), 1)
        attrs = parser.buttons[0]
        self.assertEqual(attrs.get("type"), "button")
        self.assertEqual(attrs.get("aria-pressed"), "false")
        self.assertIn("hidden", attrs)
        self.assertIn("data-theme-toggle", attrs)

    def test_both_themes_have_css_and_hidden_control_is_respected(self) -> None:
        css = (ROOT / "assets/styles.css").read_text(encoding="utf-8")
        self.assertIn(':root[data-theme="dark"]', css)
        self.assertIn("color-scheme: dark", css)
        self.assertIn("[hidden]", css)
        self.assertIn("display: none !important", css)
        self.assertIn(".theme-toggle:focus-visible", css)


if __name__ == "__main__":
    unittest.main()
