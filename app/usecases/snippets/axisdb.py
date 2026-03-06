from __future__ import annotations


def axisdb_install_prompt_markdown() -> str:
    """AxisDB: HTML block injected after the Problem→Solution→Impact section."""

    # Keep this as line-wrapped Python source for Flake8 while still emitting
    # stable HTML.
    svg_path_d = (
        "M16 1H6a2 2 0 0 0-2 2v12h2V3h10V1"
        "Zm3 4H10a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h9"
        "a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2Zm0 16H10V7h9v14Z"
    )

    lines: list[str] = [
        '<div class="fake-terminal fake-terminal--axisdb-install" '
        'aria-label="Install AxisDB">',
        '  <div class="fake-terminal__title">',
        "    <span>bash</span>",
        "    <button",
        '      class="code-copy code-copy--icon"',
        '      type="button"',
        '      data-copy-target="axisdb-install-commands"',
        '      aria-label="Copy install commands"',
        '      title="Copy install commands"',
        "    >",
        '      <svg class="code-copy__icon" viewBox="0 0 24 24" '
        'aria-hidden="true" focusable="false">',
        "        <path",
        f'          d="{svg_path_d}"',
        "        />",
        "      </svg>",
        "    </button>",
        "  </div>",
        '  <pre class="fake-terminal__body"><code>',
        '    <span class="ft-step ft-step--1">',
        '      <span class="fake-terminal__prompt">user@linux:~$ </span>',
        '      <span class="fake-terminal__typed fake-terminal__typed--1">'
        "python3 -m venv venv</span>",
        '      <span class="fake-terminal__cursor-wrap fake-terminal__cursor-wrap--1" '
        'aria-hidden="true">',
        '        <span class="fake-terminal__cursor"></span>',
        "      </span>",
        "    </span>",
        '    <span class="ft-step ft-step--2">',
        '      <span class="fake-terminal__prompt">user@linux:~$ </span>',
        '      <span class="fake-terminal__typed fake-terminal__typed--2">'
        "source venv/bin/activate</span>",
        '      <span class="fake-terminal__cursor-wrap fake-terminal__cursor-wrap--2" '
        'aria-hidden="true">',
        '        <span class="fake-terminal__cursor"></span>',
        "      </span>",
        "    </span>",
        '    <span class="ft-step ft-step--3">',
        '      <span class="fake-terminal__prompt">user@linux:~$ </span>',
        '      <span class="fake-terminal__typed fake-terminal__typed--3">'
        "pip install --upgrade pip</span>",
        '      <span class="fake-terminal__cursor-wrap fake-terminal__cursor-wrap--3" '
        'aria-hidden="true">',
        '        <span class="fake-terminal__cursor"></span>',
        "      </span>",
        "    </span>",
        '    <span class="ft-step ft-step--4">',
        '      <span class="fake-terminal__prompt">user@linux:~$ </span>',
        '      <span class="fake-terminal__typed fake-terminal__typed--4">'
        "pip install axisdb</span>",
        '      <span class="fake-terminal__cursor-wrap fake-terminal__cursor-wrap--4" '
        'aria-hidden="true">',
        '        <span class="fake-terminal__cursor"></span>',
        "      </span>",
        "    </span>",
        "  </code></pre>",
        "",
        '  <pre class="visually-hidden"><code id="axisdb-install-commands">',
        "python3 -m venv venv",
        "source venv/bin/activate",
        "pip install --upgrade pip",
        "pip install axisdb</code></pre>",
        "</div>",
    ]

    return "\n".join(lines)
