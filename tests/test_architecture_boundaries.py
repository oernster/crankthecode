"""Structural tests: the layering, held by a source scan rather than by habit.

Every other test in this suite is behavioural, so none of them can see an import
that reaches across a boundary. `ARCHITECTURE.md` states the ports/adapters
shape as an invariant; these tests are what make that statement checkable.

The scan is over the source text, not over imported modules, so a boundary
violation fails here even when the offending path is never executed.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1] / "app"

# A layer may always import from itself: a package splitting one concern across
# two modules is not a boundary crossing.
_USECASE_ALLOWED_LAYERS = {"domain", "ports", "usecases"}
_PORTS_FORBIDDEN_LAYERS = {"adapters", "http", "assets"}


def _modules_in(layer: str) -> list[Path]:
    return sorted(p for p in (APP_DIR / layer).glob("*.py"))


def _imported_modules(path: Path) -> set[str]:
    """Return every absolute module name imported by `path`."""

    tree = ast.parse(path.read_text(encoding="utf-8"))
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            # `level` is non-zero for relative imports, which carry no module
            # name to check. The package uses absolute imports throughout.
            if node.level == 0 and node.module:
                found.add(node.module)
    return found


def _app_layer_of(module: str) -> str | None:
    """Return the `app.<layer>` segment of an app import, else None."""

    parts = module.split(".")
    if len(parts) >= 2 and parts[0] == "app":
        return parts[1]
    return None


def test_domain_imports_nothing_outside_the_standard_library() -> None:
    """The domain is pure: no framework, no third-party package, no app layer.

    This is the invariant that lets the domain be reasoned about on its own.
    """

    offenders = []
    for path in _modules_in("domain"):
        for module in sorted(_imported_modules(path)):
            if module.split(".")[0] not in sys.stdlib_module_names:
                offenders.append(f"app/domain/{path.name} imports {module}")

    assert offenders == []


def test_usecases_import_only_domain_and_ports() -> None:
    """A use case depends on interfaces, never on a concrete adapter.

    Reaching past a port into `app.assets`, `app.adapters` or `app.http` means
    the use case cannot be exercised without that layer's ambient state.
    """

    offenders = []
    for path in _modules_in("usecases"):
        for module in sorted(_imported_modules(path)):
            layer = _app_layer_of(module)
            if layer is not None and layer not in _USECASE_ALLOWED_LAYERS:
                offenders.append(f"app/usecases/{path.name} imports {module}")

    assert offenders == []


def test_ports_do_not_depend_on_adapters_http_or_assets() -> None:
    """A port is an interface. Depending on an implementation inverts it."""

    offenders = []
    for path in _modules_in("ports"):
        for module in sorted(_imported_modules(path)):
            layer = _app_layer_of(module)
            if layer in _PORTS_FORBIDDEN_LAYERS:
                offenders.append(f"app/ports/{path.name} imports {module}")

    assert offenders == []


def test_the_scan_reaches_the_layers_it_claims_to_cover() -> None:
    """The invariants above are only as good as the surface they are read over.

    Renaming a layer directory would otherwise turn all three assertions into
    vacuous passes over an empty file list.
    """

    for layer in ("domain", "ports", "usecases"):
        assert _modules_in(layer), f"no modules scanned in app/{layer}"

    # And prove the parser actually yields imports, so an AST change that
    # silently returned nothing cannot make the suite green.
    assert _imported_modules(APP_DIR / "usecases" / "get_post.py")
