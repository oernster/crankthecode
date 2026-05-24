from __future__ import annotations

from app.http.view_models.posts import (
    estimate_read_time_from_template,
    estimate_read_time_minutes,
)


def test_estimate_read_time_minutes_counts_words():
    html = "<p>One two three four five six seven eight nine ten</p>"
    assert estimate_read_time_minutes(html) == 1


def test_estimate_read_time_minutes_empty_returns_one():
    assert estimate_read_time_minutes("") == 1
    assert estimate_read_time_minutes(None) == 1  # type: ignore[arg-type]


def test_estimate_read_time_from_template_reads_real_file():
    # battlestation.html exists and has substantial content; should be >= 1.
    result = estimate_read_time_from_template("battlestation.html")
    assert isinstance(result, int)
    assert result >= 1


def test_estimate_read_time_from_template_missing_file_returns_one():
    # Non-existent template must fall back to 1 rather than raising.
    result = estimate_read_time_from_template("__does_not_exist__.html")
    assert result == 1
