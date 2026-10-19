"""End-to-end tests of the translator (SCENARIOS.md, "The translator"): one test per scenario, named after its title.

Each test runs scripts/translate_content.py, as the translate-content workflow does, on a scratch copy with a small
content/ folder. The Gemini client is the stand-in in stand_ins/google/genai (no key, no network): it tags each
translation with its language and logs every call. Given = Arrange, When = Act, Then = Assert.
"""

import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
STAND_INS = Path(__file__).resolve().parent / "stand_ins"

LESSON = """---
id: "T01"
phase: 1
status: "available"
title: "Hello"
desc: "Say hello."
---
# T01: Hello

Write hello.html.
"""


def digest(text):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]


def translation(title, sha=None, body="# T01: こんにちは\n\n手で書いた翻訳。\n"):
    stamp = f'source_sha: "{sha}"\n' if sha else ""
    return f'---\ntitle: "{title}"\ndesc: "手で書いた。"\n{stamp}---\n{body}'


def scratch_repo(tmp_path, files):
    repo = tmp_path / "repo"
    shutil.copytree(ROOT / "scripts", repo / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
    for name, text in files.items():
        (repo / "content" / name).parent.mkdir(parents=True, exist_ok=True)
        (repo / "content" / name).write_text(text, encoding="utf-8")
    return repo


def translate(repo, key="test-key"):
    log = repo / "model-calls.log"
    log.touch()
    env = {**os.environ, "PYTHONPATH": str(STAND_INS), "GEMINI_API_KEY": key, "STAND_IN_LOG": str(log)}
    done = subprocess.run(
        [sys.executable, "-B", "scripts/translate_content.py"],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return done, log.read_text(encoding="utf-8").splitlines()


def read(repo, name):
    return (repo / "content" / name).read_text(encoding="utf-8")


def snapshot(repo):
    return {str(p.relative_to(repo)): p.read_bytes() for p in sorted((repo / "content").rglob("*")) if p.is_file()}


@pytest.mark.scenario("A missing translation is written and stamped with its English source")
def test_a_missing_translation_is_written_and_stamped_with_its_english_source(tmp_path):
    # Given an English lesson with no Japanese or Portuguese file
    repo = scratch_repo(tmp_path, {"tech/t01.md": LESSON})
    # When I run the translator
    done, calls = translate(repo)
    assert done.returncode == 0, done.stderr
    # Then it writes the Japanese and Portuguese files from the model's translation
    japanese, portuguese = read(repo, "tech/t01.ja.md"), read(repo, "tech/t01.pt.md")
    assert 'title: "[Japanese] Hello"' in japanese and "# [Japanese] T01: Hello" in japanese
    assert 'title: "[Portuguese (Brazilian)] Hello"' in portuguese
    assert "markdown files created: 2" in done.stdout
    # And each records the English source it was made from
    for text in (japanese, portuguese):
        assert f'source_sha: "{digest(LESSON)}"' in text


@pytest.mark.scenario("A current translation is kept as it was written")
def test_a_current_translation_is_kept_as_it_was_written(tmp_path):
    # Given an English lesson whose translations were made from its current text
    repo = scratch_repo(
        tmp_path,
        {
            "tech/t01.md": LESSON,
            "tech/t01.ja.md": translation("こんにちは", digest(LESSON)),
            "tech/t01.pt.md": translation("Olá", digest(LESSON), body="# T01: Olá\n\nTraduzido à mão.\n"),
        },
    )
    before = snapshot(repo)
    # When I run the translator
    done, calls = translate(repo)
    assert done.returncode == 0, done.stderr
    # Then the translations are unchanged and only the key check reached the model
    assert snapshot(repo) == before
    assert calls == ["ping"]
    # And it says there is nothing to do
    assert "Nothing to do." in done.stdout


@pytest.mark.scenario("A translation of an older English text is made again")
def test_a_translation_of_an_older_english_text_is_made_again(tmp_path):
    # Given a Japanese lesson made from an older version of its English source
    repo = scratch_repo(
        tmp_path,
        {
            "tech/t01.md": LESSON,
            "tech/t01.ja.md": translation("古いこんにちは", "000000000000"),
            "tech/t01.pt.md": translation("Olá", digest(LESSON)),
        },
    )
    # When I run the translator
    done, calls = translate(repo)
    assert done.returncode == 0, done.stderr
    # Then it says it retranslates that file because the source changed
    assert "RETRANSLATE (source changed) t01.ja.md" in done.stdout
    assert "t01.pt.md" not in done.stdout
    # And the file now holds a new translation stamped with the current source
    japanese = read(repo, "tech/t01.ja.md")
    assert 'title: "[Japanese] Hello"' in japanese and "古いこんにちは" not in japanese
    assert f'source_sha: "{digest(LESSON)}"' in japanese
    assert 'title: "Olá"' in read(repo, "tech/t01.pt.md")


@pytest.mark.scenario("An English-only draft is not translated")
def test_an_english_only_draft_is_not_translated(tmp_path):
    # Given an English lesson marked translate: false
    draft = LESSON.replace('desc: "Say hello."\n', 'desc: "Say hello."\ntranslate: false\n')
    repo = scratch_repo(tmp_path, {"tech/t01.md": draft})
    # When I run the translator
    done, calls = translate(repo)
    assert done.returncode == 0, done.stderr
    # Then no translation file is written
    assert sorted(p.name for p in (repo / "content/tech").iterdir()) == ["t01.md"]
    assert calls == ["ping"]
    # And it lists the lesson as an English-only draft
    assert "skipped 1 English-only draft(s): t01.md" in done.stdout


@pytest.mark.scenario("Missing text in the YAML files is filled and existing text is kept")
def test_missing_text_in_the_yaml_files_is_filled_and_existing_text_is_kept(tmp_path):
    # Given ui.yaml and resources.yaml with some Japanese and Portuguese text missing
    ui = {"nav_tech": {"en": "Tech Lessons", "ja": "技術レッスン", "pt": ""}}
    resources = [{"url": "https://exercism.org/", "title_en": "Exercism", "title_pt": "Exercism (pt)"}]
    repo = scratch_repo(
        tmp_path,
        {
            "ui.yaml": yaml.safe_dump(ui, allow_unicode=True),
            "resources.yaml": yaml.safe_dump(resources, allow_unicode=True),
        },
    )
    # When I run the translator
    done, calls = translate(repo)
    assert done.returncode == 0, done.stderr
    assert "yaml files updated:     2" in done.stdout
    ui_after = yaml.safe_load(read(repo, "ui.yaml"))
    resources_after = yaml.safe_load(read(repo, "resources.yaml"))
    # Then the missing text is filled from the model
    assert ui_after["nav_tech"]["pt"] == "[Portuguese (Brazilian)] Tech Lessons"
    assert resources_after[0]["title_ja"] == "[Japanese] Exercism"
    # And the text that was there is unchanged
    assert ui_after["nav_tech"]["ja"] == "技術レッスン"
    assert resources_after[0]["title_pt"] == "Exercism (pt)"
    assert resources_after[0]["url"] == "https://exercism.org/"


@pytest.mark.scenario("A rejected API key stops the run and says what to do")
def test_a_rejected_api_key_stops_the_run_and_says_what_to_do(tmp_path):
    # Given a GEMINI_API_KEY the API rejects
    repo = scratch_repo(tmp_path, {"tech/t01.md": LESSON})
    before = snapshot(repo)
    # When I run the translator
    done, calls = translate(repo, key="rejected-key")
    # Then it stops with an error that says the key was rejected and how to replace it
    assert done.returncode == 2
    assert "GEMINI_API_KEY was rejected by the API (status 401)" in done.stderr
    assert "Update the GEMINI_API_KEY secret" in done.stderr
    # And no file is written
    assert snapshot(repo) == before
    assert calls == ["ping"]
