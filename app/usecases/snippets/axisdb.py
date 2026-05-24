from __future__ import annotations


def axisdb_install_prompt_markdown() -> str:
    """AxisDB: HTML block injected after the Problem→Solution→Impact section."""

    # Keep this as line-wrapped Python source for Flake8 while still emitting
    # stable HTML.
    #
    # IMPORTANT: all content inside <pre class="fake-terminal__body"><code>…</code></pre>
    # must be on a single line with no extra whitespace between spans.  A <pre> element
    # preserves ALL whitespace (newlines, leading spaces) as visible text, so any
    # indentation or line-breaks inside the <code> block appear as blank lines in the
    # rendered terminal - breaking the animation effect.
    svg_path_d = (
        "M16 1H6a2 2 0 0 0-2 2v12h2V3h10V1"
        "Zm3 4H10a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h9"
        "a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2Zm0 16H10V7h9v14Z"
    )

    # Each ft-step span and its children are concatenated without any whitespace so
    # the <pre><code> block contains no visible text nodes between steps.
    def _step(n: int, typed_class: str, command: str) -> str:
        cursor = (
            f'<span class="fake-terminal__cursor-wrap fake-terminal__cursor-wrap--{n}"'
            ' aria-hidden="true">'
            '<span class="fake-terminal__cursor"></span>'
            "</span>"
        )
        return (
            f'<span class="ft-step ft-step--{n}">'
            '<span class="fake-terminal__prompt">user@linux:~$ </span>'
            f'<span class="fake-terminal__typed {typed_class}">{command}</span>'
            f"{cursor}"
            "</span>"
        )

    steps = (
        _step(1, "fake-terminal__typed--1", "python3 -m venv venv")
        + _step(2, "fake-terminal__typed--2", "source venv/bin/activate")
        + _step(3, "fake-terminal__typed--3", "pip install --upgrade pip")
        + _step(4, "fake-terminal__typed--4", "pip install axisdb")
    )

    copy_btn = (
        "    <button\n"
        '      class="code-copy code-copy--icon"\n'
        '      type="button"\n'
        '      data-copy-target="axisdb-install-commands"\n'
        '      aria-label="Copy install commands"\n'
        '      title="Copy install commands"\n'
        "    >\n"
        f'      <svg class="code-copy__icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">\n'
        "        <path\n"
        f'          d="{svg_path_d}"\n'
        "        />\n"
        "      </svg>\n"
        "    </button>"
    )

    lines: list[str] = [
        '<div class="fake-terminal fake-terminal--axisdb-install" aria-label="Install AxisDB">',
        '  <div class="fake-terminal__title">',
        "    <span>bash</span>",
        copy_btn,
        "  </div>",
        # No whitespace inside <pre><code> - all ft-step spans on one line.
        f'  <pre class="fake-terminal__body"><code>{steps}</code></pre>',
        "",
        '  <pre class="visually-hidden"><code id="axisdb-install-commands">',
        "python3 -m venv venv",
        "source venv/bin/activate",
        "pip install --upgrade pip",
        "pip install axisdb</code></pre>",
        "</div>",
    ]

    return "\n".join(lines)
