"""End-to-end tests of the build (SCENARIOS.md, "The build"): one test per scenario, named after its title.

Each test runs website/build.py on a scratch copy of website/ and content/, as `make build` would, and checks the
docs/ folder it leaves. Given = Arrange, When = Act, Then = Assert.
"""

import re
from pathlib import Path

import pytest
from conftest import ROOT, build, copy_site_sources

# The footer prints the year of the build; a new year alone is not a content change.
YEAR = re.compile(rb"<p>\d{4} KakkoiSchool")


def tree(folder: Path) -> dict[str, bytes]:
    return {
        str(path.relative_to(folder)): YEAR.sub(b"<p>YEAR KakkoiSchool", path.read_bytes())
        for path in sorted(folder.rglob("*"))
        if path.is_file()
    }


@pytest.mark.scenario("The committed site is what the build makes")
def test_the_committed_site_is_what_the_build_makes(tmp_path):
    # Given the content, templates and static files of this commit
    repo = copy_site_sources(tmp_path)
    # When I build the site
    done = build(repo)
    assert done.returncode == 0, done.stderr
    # Then the result is the committed docs/ folder, file for file, including CNAME and .nojekyll
    made, committed = tree(repo / "docs"), tree(ROOT / "docs")
    missing = sorted(set(committed) - set(made))
    extra = sorted(set(made) - set(committed))
    changed = sorted(name for name in set(made) & set(committed) if made[name] != committed[name])
    assert not (missing or extra or changed), (
        "docs/ is out of date: run `make build` and commit docs/ with the content change.\n"
        f"missing: {missing[:10]}\nextra: {extra[:10]}\nchanged: {changed[:10]}"
    )
    assert made["CNAME"] == b"school.kakkoi.dev\n"
    assert ".nojekyll" in made
    # And building again changes nothing
    again = build(repo)
    assert again.returncode == 0, again.stderr
    assert tree(repo / "docs") == made


@pytest.mark.scenario("A lesson with broken front matter stops the build")
def test_a_lesson_with_broken_front_matter_stops_the_build(tmp_path):
    # Given a built site and a lesson whose front matter is not valid YAML
    repo = copy_site_sources(tmp_path)
    assert build(repo).returncode == 0
    before = tree(repo / "docs")
    (repo / "content/tech/t97.md").write_text(
        '---\ntitle: "Unclosed\nphase: [1\n---\n# Broken\n', encoding="utf-8"
    )
    # When I build the site
    done = build(repo)
    # Then the build fails with the YAML error
    assert done.returncode != 0
    assert "yaml.scanner.ScannerError" in done.stderr or "yaml.parser.ParserError" in done.stderr
    # And docs/ is still the site from before
    assert tree(repo / "docs") == before


@pytest.mark.scenario("A build that fails halfway leaves the published site in place")
def test_a_build_that_fails_halfway_leaves_the_published_site_in_place(tmp_path):
    # Given a built site and a page template that includes a missing file
    repo = copy_site_sources(tmp_path)
    assert build(repo).returncode == 0
    before = tree(repo / "docs")
    page = repo / "website/pages/videos.html"
    page.write_text(page.read_text(encoding="utf-8") + '{% include "missing-part.html" %}\n', encoding="utf-8")
    # When I build the site
    done = build(repo)
    # Then the build fails and names the missing file
    assert done.returncode != 0
    assert "missing-part.html" in done.stderr
    # And docs/ is still the site from before, with no build folder left behind
    assert tree(repo / "docs") == before
    assert not list(repo.glob(".docs_build_*")) and not (repo / ".docs_old").exists()
