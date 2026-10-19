"""Fixtures for the end-to-end tests (scenarios in SCENARIOS.md).

- Tests never reach the network: Python sockets may only connect to this machine, and every browser request that
  would leave it is answered by a small stand-in page that names the address (so a link can still be followed).
- Every Chromium gets --use-mock-keychain and --password-store=basic (test-core NOTES.md 1); PLAYWRIGHT_CHROMIUM
  (or TEST_CORE_CHROME) points at an existing Chromium so nothing is downloaded.
- site / site_url: the real content/ built by website/build.py into a scratch folder and served on a free port.
- edited_site_url: the same with two extra lessons, for the coming-soon and English-fallback scenarios.
"""

from __future__ import annotations

import functools
import html
import ipaddress
import os
import shutil
import socket
import subprocess
import sys
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

import pytest

ROOT = Path(__file__).resolve().parents[2]
CHROMIUM_FLAGS = ["--use-mock-keychain", "--password-store=basic"]
LOCAL_HOSTS = {"127.0.0.1", "localhost", "::1"}

_connect = socket.socket.connect


def _is_local(address) -> bool:
    if not isinstance(address, tuple):
        return True
    if address[0] == "localhost":
        return True
    try:
        return ipaddress.ip_address(address[0]).is_loopback
    except ValueError:
        return False


def _guarded_connect(self, address):
    if not _is_local(address):
        raise OSError(f"tests never reach the network (tried {address!r}); use a stand-in")
    return _connect(self, address)


@pytest.fixture(autouse=True)
def _no_network(monkeypatch):
    monkeypatch.setattr(socket.socket, "connect", _guarded_connect)


# -- the site -----------------------------------------------------------------


def copy_site_sources(target: Path) -> Path:
    """website/ and content/ copied to target, so a build there writes target/docs and leaves the checkout alone."""
    for name in ("website", "content"):
        shutil.copytree(ROOT / name, target / name, ignore=shutil.ignore_patterns("__pycache__"))
    return target


def build(repo: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-B", "website/build.py"],
        cwd=repo,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def built(repo: Path) -> Path:
    done = build(repo)
    assert done.returncode == 0, done.stderr
    return repo / "docs"


@functools.cache
def _quiet_handler(directory: str):
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=directory, **kwargs)

        def log_message(self, *args):
            pass

    return Handler


@pytest.fixture(scope="session")
def serve():
    servers = []

    def start(folder: Path) -> str:
        server = ThreadingHTTPServer(("127.0.0.1", 0), _quiet_handler(str(folder)))
        threading.Thread(target=server.serve_forever, daemon=True).start()
        servers.append(server)
        return f"http://127.0.0.1:{server.server_port}"

    yield start
    for server in servers:
        server.shutdown()
        server.server_close()


@pytest.fixture(scope="session")
def site(tmp_path_factory) -> Path:
    """The real content, built fresh into a scratch folder."""
    return built(copy_site_sources(tmp_path_factory.mktemp("site")))


@pytest.fixture(scope="session")
def site_url(site, serve) -> str:
    return serve(site)


COMING_SOON = """---
id: "T99"
phase: 1
status: "coming-soon"
title: "Lesson From The Future"
desc: "Not written yet."
---
"""

ENGLISH_ONLY = """---
id: "T98"
phase: 1
status: "available"
title: "Only In English"
desc: "A lesson nobody translated yet."
translate: false
---
# T98: Only In English

This paragraph exists only in English.
"""


@pytest.fixture(scope="session")
def edited_site_url(tmp_path_factory, serve) -> str:
    repo = copy_site_sources(tmp_path_factory.mktemp("edited-site"))
    (repo / "content/tech/t99.md").write_text(COMING_SOON, encoding="utf-8")
    (repo / "content/tech/t98.md").write_text(ENGLISH_ONLY, encoding="utf-8")
    return serve(built(repo))


# -- the browser ----------------------------------------------------------------


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    args = {
        **browser_type_launch_args,
        "args": [*browser_type_launch_args.get("args", []), *CHROMIUM_FLAGS],
    }
    chrome = os.environ.get("PLAYWRIGHT_CHROMIUM") or os.environ.get("TEST_CORE_CHROME")
    if chrome:
        args["executable_path"] = chrome
    return args


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "color_scheme": "light", "locale": "en-US"}


def stand_in(route):
    """Answer a request that would leave this machine: a page naming the address, or an empty file."""
    if urlsplit(route.request.url).hostname in LOCAL_HOSTS:
        route.fallback()
    elif route.request.resource_type == "document":
        address = html.escape(route.request.url)
        body = f"<!doctype html><title>Stand-in</title><h1>Stand-in for {address}</h1>"
        route.fulfill(status=200, content_type="text/html", body=body)
    else:
        route.fulfill(status=200, content_type="text/plain", body="")


@pytest.fixture
def context(context):
    context.route("**/*", stand_in)
    yield context
