"""End-to-end tests of the site (SCENARIOS.md, "The site"): one test per scenario, named after its title.

Playwright drives the site built from content/ (fixtures in conftest.py) the way a learner uses it: by role, label
and visible text. Given = Arrange, When = Act, Then = Assert.
"""

import re
from pathlib import Path

import pytest
import yaml
from playwright.sync_api import expect

ROOT = Path(__file__).resolve().parents[2]
SECTIONS = [  # (link text, page heading, page file)
    ("Tech Lessons", "Technical Lessons", "tech-lessons.html"),
    ("Theory", "Theory & Life Lessons", "theory-lessons.html"),
    ("AI Lessons", "AI Lessons", "ai-lessons.html"),
    ("The Workbench", "The Workbench", "workbench-lessons.html"),
    ("Videos", "Lesson Videos", "videos.html"),
    ("Resources", "Resources", "resources.html"),
]


def content_yaml(name):
    return yaml.safe_load((ROOT / "content" / name).read_text(encoding="utf-8"))


def top_nav(page):
    return page.locator("nav.site-nav")


def exactly(text):
    """A heading's whole name; the stylesheet adds " #" to every heading anchor."""
    return re.compile(rf"^{re.escape(text)}( #)?$")


def heading(page, text):
    return page.get_by_role("heading", level=1, name=exactly(text))


@pytest.mark.scenario("Start Learning opens the technical lessons")
def test_start_learning_opens_the_technical_lessons(page, site_url):
    # Given the home page in English
    page.goto(f"{site_url}/index.html")
    expect(heading(page, "Learn to Build the Web")).to_be_visible()
    # When I press Start Learning
    page.get_by_role("link", name="Start Learning").click()
    # Then I am on the Technical Lessons page
    expect(page).to_have_url(f"{site_url}/tech-lessons.html")
    expect(heading(page, "Technical Lessons")).to_be_visible()
    # And it lists T01 Environment Setup
    expect(page.get_by_role("link", name="T01 Environment Setup")).to_be_visible()


@pytest.mark.scenario("The home page cards lead to every section")
def test_the_home_page_cards_lead_to_every_section(page, site_url):
    for link, title, file in SECTIONS:
        # Given the home page in English
        page.goto(f"{site_url}/index.html")
        # When I open each section card in turn
        page.locator(".sections-grid").get_by_role("link", name=link).click()
        # Then each card opens its section
        expect(page).to_have_url(f"{site_url}/{file}")
        expect(heading(page, title)).to_be_visible()


@pytest.mark.scenario("The top navigation reaches every section")
def test_the_top_navigation_reaches_every_section(page, site_url):
    # Given any page of the site
    page.goto(f"{site_url}/lessons/t01.html")
    # When I use each link of the top navigation in turn, then the KakkoiSchool logo
    for link, title, file in SECTIONS:
        top_nav(page).get_by_role("link", name=link, exact=True).click()
        # Then each link opens its section
        expect(page).to_have_url(f"{site_url}/{file}")
        expect(heading(page, title)).to_be_visible()
    top_nav(page).get_by_role("link", name="KakkoiSchool").click()
    # And the logo brings me back to the home page
    expect(page).to_have_url(f"{site_url}/index.html")
    expect(heading(page, "Learn to Build the Web")).to_be_visible()


@pytest.mark.scenario("Every lesson list opens its first lesson")
def test_every_lesson_list_opens_its_first_lesson(page, site_url):
    lists = [
        ("tech-lessons.html", "T01 Environment Setup", "T01: Environment Setup", "Back to Tech Lessons"),
        ("theory-lessons.html", "R01 What is IT?", "R01: What is IT?", "Back to Theory Lessons"),
        ("ai-lessons.html", "A01 AI Risks + Set Up Your Environment", "A01:", "Back to AI Lessons"),
        ("workbench-lessons.html", "W01 What the Workbench Is", "W01:", "Back to The Workbench"),
    ]
    for file, card, title, back in lists:
        # Given the Tech, Theory, AI and Workbench lesson lists
        page.goto(f"{site_url}/{file}")
        # When I open the first lesson card of each list
        page.get_by_role("link", name=card).click()
        # Then the lesson page shows that lesson's title
        expect(page).to_have_url(re.compile(r"/lessons/[a-z]01\.html$"))
        expect(page.get_by_role("heading", level=1)).to_contain_text(title)
        # And its back link names the list it came from
        page.get_by_role("link", name=back).first.click()
        expect(page).to_have_url(f"{site_url}/{file}")


@pytest.mark.scenario("Next, Previous and Back move through the lessons")
def test_next_previous_and_back_move_through_the_lessons(page, site_url):
    # Given the first technical lesson, T01
    page.goto(f"{site_url}/lessons/t01.html")
    lesson_title = page.get_by_role("heading", level=1)
    expect(lesson_title).to_contain_text("T01: Environment Setup")
    # And T01 offers no Previous link
    expect(page.get_by_role("link", name="Previous", exact=True)).to_have_count(0)
    # When I press Next, then Previous, then Back to Tech Lessons
    page.get_by_role("link", name="Next", exact=True).first.click()
    # Then I see T02, then T01 again, then the Technical Lessons list
    expect(lesson_title).to_contain_text("T02: Terminal Basics")
    page.get_by_role("link", name="Previous", exact=True).first.click()
    expect(lesson_title).to_contain_text("T01: Environment Setup")
    page.get_by_role("link", name="Back to Tech Lessons").first.click()
    expect(page).to_have_url(f"{site_url}/tech-lessons.html")


@pytest.mark.scenario("Switching the language keeps me on the same page")
def test_switching_the_language_keeps_me_on_the_same_page(page, site_url):
    # Given the Technical Lessons page in English
    page.goto(f"{site_url}/tech-lessons.html")
    language = page.get_by_role("combobox", name="Language")
    # When I choose 日本語 in the language menu
    language.select_option(label="日本語")
    # Then I see the same page in Japanese
    expect(page).to_have_url(f"{site_url}/ja/tech-lessons.html")
    expect(page.locator("html")).to_have_attribute("lang", "ja")
    expect(heading(page, "技術レッスン")).to_be_visible()
    # When I choose Português on a lesson
    page.goto(f"{site_url}/ja/lessons/t01.html")
    language.select_option(label="Português")
    # Then the same lesson in Portuguese
    expect(page).to_have_url(f"{site_url}/pt/lessons/t01.html")
    expect(page.get_by_role("heading", level=1)).to_contain_text("Configuração do Ambiente")
    # When I choose English, then the lesson in English
    language.select_option(label="English")
    expect(page).to_have_url(f"{site_url}/lessons/t01.html")
    expect(page.get_by_role("heading", level=1)).to_contain_text("Environment Setup")


@pytest.mark.scenario("The theme button switches the theme and remembers it")
def test_the_theme_button_switches_the_theme_and_remembers_it(page, site_url):
    # Given the home page in the light theme
    page.goto(f"{site_url}/index.html")
    root = page.locator("html")
    expect(root).to_have_attribute("data-theme", "light")
    # When I press Toggle theme
    page.get_by_role("button", name="Toggle theme").click()
    # Then the page is dark
    expect(root).to_have_attribute("data-theme", "dark")
    # And it is still dark after a reload and on the next page I open
    page.reload()
    expect(root).to_have_attribute("data-theme", "dark")
    top_nav(page).get_by_role("link", name="Resources", exact=True).click()
    expect(heading(page, "Resources")).to_be_visible()
    expect(root).to_have_attribute("data-theme", "dark")


@pytest.mark.scenario("On a phone the menu button shows the sections")
def test_on_a_phone_the_menu_button_shows_the_sections(page, site_url):
    # Given the home page on a phone-sized screen
    page.set_viewport_size({"width": 390, "height": 844})
    page.goto(f"{site_url}/index.html")
    videos = top_nav(page).get_by_role("link", name="Videos", exact=True)
    expect(videos).to_be_hidden()
    # When I press Menu
    page.get_by_role("button", name="Menu").click()
    # Then the section links appear
    for link, _title, _file in SECTIONS:
        expect(top_nav(page).get_by_role("link", name=link, exact=True)).to_be_visible()
    # And Videos opens the Lesson Videos page
    videos.click()
    expect(heading(page, "Lesson Videos")).to_be_visible()


@pytest.mark.scenario("A lesson heading links to itself")
def test_a_lesson_heading_links_to_itself(page, site_url):
    # Given a lesson page
    page.goto(f"{site_url}/lessons/t01.html")
    section = page.get_by_role("heading", level=2, name="Install VS Code")
    expect(section).to_have_attribute("id", "install-vs-code")
    # When I click one of its section headings
    section.get_by_role("link", name="Install VS Code").click()
    # Then the address ends with that heading's anchor
    expect(page).to_have_url(f"{site_url}/lessons/t01.html#install-vs-code")


@pytest.mark.scenario("The videos page shows every video")
def test_the_videos_page_shows_every_video(page, site_url):
    videos = content_yaml("videos.yaml")
    # Given the Lesson Videos page
    page.goto(f"{site_url}/videos.html")
    # When it has loaded
    expect(heading(page, "Lesson Videos")).to_be_visible()
    # Then it shows one video player and one title for each video in content/videos.yaml
    expect(page.locator(".video-card iframe")).to_have_count(len(videos))
    for video in videos:
        player = page.locator(f'iframe[title="{video["title_en"]}"]')
        expect(player).to_have_attribute("src", f"https://www.youtube.com/embed/{video['youtube_id']}")
        expect(page.get_by_role("heading", level=3, name=exactly(video["title_en"]))).to_be_visible()


@pytest.mark.scenario("Every resource opens in a new tab")
def test_every_resource_opens_in_a_new_tab(page, site_url):
    resources = content_yaml("resources.yaml")
    # Given the Resources page
    page.goto(f"{site_url}/resources.html")
    first = resources[0]
    # When I open a resource card
    with page.expect_popup() as popup:
        page.get_by_role("link", name=first["title_en"]).first.click()
    # Then the resource opens in a new tab at its address
    expect(popup.value).to_have_url(first["url"])
    expect(page).to_have_url(f"{site_url}/resources.html")
    # And every card shows the domain of its resource
    cards = page.locator(".resource-card")
    expect(cards).to_have_count(len(resources))
    for index, resource in enumerate(resources):
        expect(cards.nth(index)).to_have_attribute("href", resource["url"])
        expect(cards.nth(index)).to_have_attribute("target", "_blank")
        expect(cards.nth(index).locator(".resource-url")).to_have_text(resource["domain"])


@pytest.mark.scenario("The footer and the Discord button lead to the community and the licences")
def test_the_footer_and_the_discord_button_lead_to_the_community_and_the_licences(page, site_url):
    repo = "https://github.com/KakkoiDev/izumo-io"
    # Given the home page
    page.goto(f"{site_url}/index.html")
    # When I use Join our Discord
    with page.expect_popup() as popup:
        page.get_by_role("link", name="Join our Discord").click()
    # Then Join our Discord opens the Discord invite in a new tab
    expect(popup.value).to_have_url("https://discord.gg/YrtdssGUJa")
    # When I use the footer links Discord, GitHub, CC BY 4.0 and MIT
    footer = page.locator("footer")
    targets = [
        ("Discord", "https://discord.gg/YrtdssGUJa"),
        ("GitHub", repo),
        ("CC BY 4.0", f"{repo}/blob/master/LICENSE"),
        ("MIT", f"{repo}/blob/master/LICENSE-CODE"),
    ]
    for name, address in targets:
        page.goto(f"{site_url}/index.html")
        footer.get_by_role("link", name=name, exact=True).click()
        # Then the footer links open the Discord invite, the repository and the two licence files
        expect(page).to_have_url(address)
        expect(page.get_by_role("heading", name=f"Stand-in for {address}")).to_be_visible()


@pytest.mark.scenario("Every page has a Markdown copy")
def test_every_page_has_a_markdown_copy(page, site_url):
    # Given the built site
    # When I ask for a page or a lesson with .md instead of .html
    listing = page.request.get(f"{site_url}/tech-lessons.md")
    lesson = page.request.get(f"{site_url}/ja/lessons/t01.md")
    # Then I get the page as Markdown with links to the lessons' Markdown copies
    assert listing.ok
    text = listing.text()
    assert text.startswith("# Technical Lessons\n")
    assert "- [T01: Environment Setup](lessons/t01.md)" in text
    # And a lesson's Markdown copy is its source file from content/
    assert lesson.ok
    assert lesson.body().decode("utf-8") == (ROOT / "content/tech/t01.ja.md").read_text(encoding="utf-8")


@pytest.mark.scenario("A coming-soon lesson is listed but cannot be opened")
def test_a_coming_soon_lesson_is_listed_but_cannot_be_opened(page, edited_site_url):
    # Given content with a technical lesson marked coming-soon
    # When I open the Technical Lessons page
    page.goto(f"{edited_site_url}/tech-lessons.html")
    # Then the lesson is listed with a Coming Soon badge
    card = page.locator(".lesson-card.coming-soon").filter(has_text="Lesson From The Future")
    expect(card).to_be_visible()
    expect(card.get_by_text("Coming Soon")).to_be_visible()
    # And it is not a link and has no page
    expect(page.get_by_role("link", name="T99 Lesson From The Future")).to_have_count(0)
    assert page.request.get(f"{edited_site_url}/lessons/t99.html").status == 404


@pytest.mark.scenario("A lesson without a translation shows the English text")
def test_a_lesson_without_a_translation_shows_the_english_text(page, edited_site_url):
    # Given content with a lesson that exists only in English
    # When I open that lesson in Japanese
    page.goto(f"{edited_site_url}/ja/lessons/t98.html")
    # Then I read the English lesson text
    expect(page.get_by_role("heading", level=1)).to_have_text("T98: Only In English")
    expect(page.get_by_text("This paragraph exists only in English.")).to_be_visible()
    # And the navigation around it is in Japanese
    expect(page.locator("html")).to_have_attribute("lang", "ja")
    expect(page.get_by_role("link", name="技術レッスンに戻る").first).to_be_visible()
    expect(top_nav(page).get_by_role("link", name="技術レッスン", exact=True)).to_be_visible()
