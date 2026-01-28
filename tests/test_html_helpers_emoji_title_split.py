from __future__ import annotations

from app.http.routers.html import _display_title_parts, _split_leading_emoji_from_title


def test_split_leading_emoji_from_title_handles_blank_and_non_emoji():
    assert _split_leading_emoji_from_title("") == (None, "")
    assert _split_leading_emoji_from_title("   ") == (None, "")
    assert _split_leading_emoji_from_title("Hello world") == (None, "Hello world")


def test_split_leading_emoji_from_title_handles_long_first_token_guard():
    # Any first token longer than 6 codepoints should not be treated as an emoji.
    # (This primarily exists to avoid mis-classifying non-emoji strings.)
    title = "abcdefghijk rest"
    assert _split_leading_emoji_from_title(title) == (None, title)


def test_split_leading_emoji_from_title_extracts_emoji_and_remaining_text():
    assert _split_leading_emoji_from_title("🧪 Hello") == ("🧪", "Hello")
    # Emoji-only title returns the emoji but keeps a non-empty title_text.
    assert _split_leading_emoji_from_title("🧪") == ("🧪", "🧪")


def test_display_title_parts_prefers_explicit_frontmatter_emoji_and_strips_title():
    assert _display_title_parts(title="  Hello  ", emoji=" 🔥 ") == ("🔥", "Hello")


def test_display_title_parts_falls_back_to_title_emoji_when_no_explicit_emoji():
    assert _display_title_parts(title="🧠 Brain", emoji=None) == ("🧠", "Brain")
    assert _display_title_parts(title="Plain", emoji=None) == ("", "Plain")

