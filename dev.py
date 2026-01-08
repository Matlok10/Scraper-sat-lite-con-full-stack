#!/usr/bin/env python3
"""
Dev CLI for the Recos project.

Centralizes common development tasks so you don't need to remember long commands.
Works without activating the venv by always invoking the venv's python.

Usage examples:
  - python dev.py setup              # Create venv (if missing) + install deps
  - python dev.py runserver          # Start Django dev server
  - python dev.py migrate            # Apply migrations
  - python dev.py makemigrations     # Make migrations
  - python dev.py test [app]         # Run tests (all or specific app)
  - python dev.py shell              # Django shell
  - python dev.py collectstatic      # Collect static files
  - python dev.py sh                 # Open an interactive shell with venv activated
  - python dev.py print-activate     # Print 'source' command to activate venv in current shell
"""
from __future__ import annotations

import argparse
import os
import platform
import shlex
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BACKEND_DIR = ROOT / "backend"
MANAGE_PY = BACKEND_DIR / "manage.py"
VENV_DIR = ROOT / "venv"

IS_WINDOWS = platform.system().lower().startswith("win")
VENV_PY = VENV_DIR / ("Scripts/python.exe" if IS_WINDOWS else "bin/python")
VENV_PIP = VENV_DIR / ("Scripts/pip.exe" if IS_WINDOWS else "bin/pip")
VENV_ACTIVATE = VENV_DIR / ("Scripts/activate" if IS_WINDOWS else "bin/activate")


def run(cmd: list[str] | str, cwd: Path | None = None, env: dict | None = None, check: bool = True) -> int:
    if isinstance(cmd, str):
        print(f"$ {cmd}")
        return subprocess.run(cmd, shell=True, cwd=str(cwd) if cwd else None, env=env, check=check).returncode
    else:
        print("$ " + " ".join(shlex.quote(str(c)) for c in cmd))
        return subprocess.run(cmd, cwd=str(cwd) if cwd else None, env=env, check=check).returncode


def ensure_manage_py():
    if not MANAGE_PY.exists():
        sys.exit(f"ERROR: manage.py not found at {MANAGE_PY}")


def ensure_python():
    # Try to locate python3 if default python is not 3.x
    py = sys.executable
    if not py:
        sys.exit("ERROR: Could not determine current Python interpreter.")
    return py


def ensure_venv() -> None:
    if VENV_PY.exists():
        return
    print("🔧 Creating virtual environment in ./venv ...")
    py = ensure_python()
    run([py, "-m", "venv", str(VENV_DIR)])
    print("✅ venv created.")


def pip_install(requirements: str = str(BACKEND_DIR / "requirements.txt")) -> None:
    if not VENV_PIP.exists():
        ensure_venv()
    print("🔧 Upgrading pip/setuptools/wheel ...")
    run([str(VENV_PY), "-m", "pip", "install", "-U", "pip", "setuptools", "wheel"])
    if requirements and Path(requirements).exists():
        print(f"📦 Installing dependencies from {requirements} ...")
        run([str(VENV_PY), "-m", "pip", "install", "-r", requirements])
    else:
        print("ℹ️ No requirements.txt found; skipping dependency install.")


def manage(*args: str, passthrough: list[str] | None = None, check: bool = True) -> int:
    ensure_manage_py()
    ensure_venv()
    cmd = [str(VENV_PY), str(MANAGE_PY), *args]
    if passthrough:
        cmd += list(passthrough)
    return run(cmd, cwd=BACKEND_DIR, check=check)


def cmd_setup(_: argparse.Namespace) -> None:
    ensure_venv()
    pip_install()
    print("\n✅ Setup complete. Quick start:")
    print("  - python dev.py runserver")
    print("  - python dev.py print-activate  # to activate in your shell")


def cmd_install(args: argparse.Namespace) -> None:
    pip_install(args.requirements)


def cmd_runserver(args: argparse.Namespace) -> None:
    manage("runserver", passthrough=args.extra)


def cmd_migrate(_: argparse.Namespace) -> None:
    manage("migrate")


def cmd_makemigrations(args: argparse.Namespace) -> None:
    if args.app:
        manage("makemigrations", args.app)
    else:
        manage("makemigrations")


def cmd_shell(_: argparse.Namespace) -> None:
    manage("shell")


def cmd_createsuperuser(_: argparse.Namespace) -> None:
    manage("createsuperuser")


def cmd_test(args: argparse.Namespace) -> None:
    if args.app:
        manage("test", args.app, passthrough=args.extra)
    else:
        manage("test", passthrough=args.extra)


def cmd_collectstatic(args: argparse.Namespace) -> None:
    extra = ["--noinput"] + (args.extra or [])
    manage("collectstatic", passthrough=extra)


def cmd_check(_: argparse.Namespace) -> None:
    manage("check")


def cmd_loaddata(args: argparse.Namespace) -> None:
    if not args.fixtures:
        print("Usage: dev.py loaddata <fixture1> [fixture2 ...]")
        return
    manage("loaddata", passthrough=args.fixtures)


def cmd_clearsessions(_: argparse.Namespace) -> None:
    manage("clearsessions")


def cmd_load_sample(_: argparse.Namespace) -> None:
    """Load the default sample fixture (fixtures/sample_data.json)."""
    fixture_path = ROOT / "backend" / "fixtures" / "sample_data.json"
    if not fixture_path.exists():
        print(f"Fixture not found: {fixture_path}")
        return
    manage("loaddata", passthrough=[str(fixture_path)])


def cmd_sh(_: argparse.Namespace) -> None:
    """Open an interactive shell with the venv activated."""
    ensure_venv()
    if IS_WINDOWS:
        # On Windows, open cmd with venv activated
        activation = str(VENV_ACTIVATE)
        print("Opening cmd with venv active (Windows)...")
        # Best-effort approach; users can manually activate if needed
        run(["cmd.exe", "/K", f"call {activation}"])
    else:
        bash = os.environ.get("SHELL", "/bin/bash")
        rc = f"source {shlex.quote(str(VENV_ACTIVATE))}; echo '(venv) activated → {bash}'; exec {shlex.quote(bash)} -i"
        run([bash, "-i", "-c", rc], cwd=ROOT, check=False)


def cmd_print_activate(_: argparse.Namespace) -> None:
    if IS_WINDOWS:
        print(fr"activate venv: {VENV_DIR}\Scripts\activate")
    else:
        print(f"source {VENV_ACTIVATE}")


def cmd_info(_: argparse.Namespace) -> None:
    print("Project info:\n" + "-" * 40)
    print(f"ROOT:           {ROOT}")
    print(f"BACKEND_DIR:    {BACKEND_DIR}")
    print(f"MANAGE_PY:      {MANAGE_PY}  ({'OK' if MANAGE_PY.exists() else 'MISSING'})")
    print(f"VENV_PY:        {VENV_PY}  ({'OK' if VENV_PY.exists() else 'MISSING'})")
    if VENV_PY.exists():
        run([str(VENV_PY), "-V"], check=False)
        run([str(VENV_PY), "-m", "pip", "--version"], check=False)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Recos Dev CLI")
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("setup", help="Create venv (if missing) and install dependencies")
    s.set_defaults(func=cmd_setup)

    s = sub.add_parser("install", help="Install dependencies from requirements.txt")
    s.add_argument("--requirements", "-r", default=str(BACKEND_DIR / "requirements.txt"), help="Path to requirements.txt")
    s.set_defaults(func=cmd_install)

    s = sub.add_parser("runserver", help="Run Django development server")
    s.add_argument("extra", nargs=argparse.REMAINDER, help="Extra args forwarded to runserver, e.g. 0.0.0.0:8000")
    s.set_defaults(func=cmd_runserver)

    s = sub.add_parser("migrate", help="Apply database migrations")
    s.set_defaults(func=cmd_migrate)

    s = sub.add_parser("makemigrations", help="Create new migrations")
    s.add_argument("app", nargs="?", help="App label (optional)")
    s.set_defaults(func=cmd_makemigrations)

    s = sub.add_parser("shell", help="Open Django shell")
    s.set_defaults(func=cmd_shell)

    s = sub.add_parser("createsuperuser", help="Create a superuser")
    s.set_defaults(func=cmd_createsuperuser)

    s = sub.add_parser("test", help="Run tests (all or a single app)")
    s.add_argument("app", nargs="?", help="App label (optional)")
    s.add_argument("extra", nargs=argparse.REMAINDER, help="Extra pytest/test args")
    s.set_defaults(func=cmd_test)

    s = sub.add_parser("collectstatic", help="Collect static files to STATIC_ROOT")
    s.add_argument("extra", nargs=argparse.REMAINDER, help="Extra args for collectstatic")
    s.set_defaults(func=cmd_collectstatic)

    s = sub.add_parser("check", help="Run Django system checks")
    s.set_defaults(func=cmd_check)

    s = sub.add_parser("loaddata", help="Load fixture data via manage.py loaddata")
    s.add_argument("fixtures", nargs=argparse.ONE_OR_MORE, help="Fixture paths")
    s.set_defaults(func=cmd_loaddata)

    s = sub.add_parser("clearsessions", help="Purge expired sessions")
    s.set_defaults(func=cmd_clearsessions)

    s = sub.add_parser("load-sample", help="Load default sample fixture for quick demo data")
    s.set_defaults(func=cmd_load_sample)

    s = sub.add_parser("sh", help="Open an interactive shell with the venv activated")
    s.set_defaults(func=cmd_sh)

    s = sub.add_parser("print-activate", help="Print the command to activate venv in your shell")
    s.set_defaults(func=cmd_print_activate)

    s = sub.add_parser("info", help="Show project/venv info")
    s.set_defaults(func=cmd_info)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        args.func(args)
        return 0
    except subprocess.CalledProcessError as e:
        return e.returncode


if __name__ == "__main__":
    raise SystemExit(main())
