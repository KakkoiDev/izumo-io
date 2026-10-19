# Scenarios

What the KakkoiSchool site and this repository's commands do for a person, in Given/When/Then. Each scenario is one
end-to-end test in `tests/e2e/`, named exactly after its title (`@pytest.mark.scenario("<title>")` on
`def test_<title in snake case>`):

- the site: [tests/e2e/test_site.py](tests/e2e/test_site.py), Playwright on a fresh build of `content/` served
  from this machine; every request that would leave it gets a stand-in page, so the tests run offline;
- the build: [tests/e2e/test_build.py](tests/e2e/test_build.py), `website/build.py` on a scratch copy;
- the translator: [tests/e2e/test_translate.py](tests/e2e/test_translate.py), `scripts/translate_content.py` on a
  scratch `content/` with a stand-in for the Gemini client (no key, no network).

`python -m pytest` runs them; the whole gate (scenario check, control coverage, flaky lint) is in
[AGENTS.md](AGENTS.md). Adding a feature: write its scenario here
first, then its test (red), then the change (green). Removing one: remove its scenario and its test in the same
commit, and say so in the message.

Not covered on purpose: `scripts/extract_content.py` (a one-shot migration that imports `website/lessons.py`, which
no longer exists), the `Makefile` targets (thin wrappers around the build and `python -m http.server`), and the
learner material under `courses/` and `submissions/` (not part of the site).

## The site

### Scenario: Start Learning opens the technical lessons
Given the home page in English
When I press Start Learning
Then I am on the Technical Lessons page
And it lists T01 Environment Setup

### Scenario: The home page cards lead to every section
Given the home page in English
When I open each section card in turn
Then each card opens its section: Tech Lessons, Theory, AI Lessons, The Workbench, Videos and Resources

### Scenario: The top navigation reaches every section
Given any page of the site
When I use each link of the top navigation in turn, then the KakkoiSchool logo
Then each link opens its section
And the logo brings me back to the home page

### Scenario: Every lesson list opens its first lesson
Given the Tech, Theory, AI and Workbench lesson lists
When I open the first lesson card of each list
Then the lesson page shows that lesson's title
And its back link names the list it came from

### Scenario: Next, Previous and Back move through the lessons
Given the first technical lesson, T01
When I press Next, then Previous, then Back to Tech Lessons
Then I see T02, then T01 again, then the Technical Lessons list
And T01 offers no Previous link

### Scenario: Switching the language keeps me on the same page
Given the Technical Lessons page in English
When I choose 日本語 in the language menu, then Português on a lesson, then English
Then I see the same page in Japanese, then the same lesson in Portuguese, then the lesson in English

### Scenario: The theme button switches the theme and remembers it
Given the home page in the light theme
When I press Toggle theme
Then the page is dark
And it is still dark after a reload and on the next page I open

### Scenario: On a phone the menu button shows the sections
Given the home page on a phone-sized screen
When I press Menu
Then the section links appear
And Videos opens the Lesson Videos page

### Scenario: A lesson heading links to itself
Given a lesson page
When I click one of its section headings
Then the address ends with that heading's anchor

### Scenario: The videos page shows every video
Given the Lesson Videos page
When it has loaded
Then it shows one video player and one title for each video in content/videos.yaml

### Scenario: Every resource opens in a new tab
Given the Resources page
When I open a resource card
Then the resource opens in a new tab at its address
And every card shows the domain of its resource

### Scenario: The footer and the Discord button lead to the community and the licences
Given the home page
When I use Join our Discord, then the footer links Discord, GitHub, CC BY 4.0 and MIT
Then Join our Discord opens the Discord invite in a new tab
And the footer links open the Discord invite, the repository and the two licence files

### Scenario: Every page has a Markdown copy
Given the built site
When I ask for a page or a lesson with .md instead of .html
Then I get the page as Markdown with links to the lessons' Markdown copies
And a lesson's Markdown copy is its source file from content/

### Scenario: A coming-soon lesson is listed but cannot be opened
Given content with a technical lesson marked coming-soon
When I open the Technical Lessons page
Then the lesson is listed with a Coming Soon badge
And it is not a link and has no page

### Scenario: A lesson without a translation shows the English text
Given content with a lesson that exists only in English
When I open that lesson in Japanese
Then I read the English lesson text
And the navigation around it is in Japanese

## The build

### Scenario: The committed site is what the build makes
Given the content, templates and static files of this commit
When I build the site
Then the result is the committed docs/ folder, file for file, including CNAME and .nojekyll
And building again changes nothing

### Scenario: A lesson with broken front matter stops the build
Given a built site and a lesson whose front matter is not valid YAML
When I build the site
Then the build fails with the YAML error
And docs/ is still the site from before

### Scenario: A build that fails halfway leaves the published site in place
Given a built site and a page template that includes a missing file
When I build the site
Then the build fails and names the missing file
And docs/ is still the site from before, with no build folder left behind

## The translator

### Scenario: A missing translation is written and stamped with its English source
Given an English lesson with no Japanese or Portuguese file
When I run the translator
Then it writes the Japanese and Portuguese files from the model's translation
And each records the English source it was made from

### Scenario: A current translation is kept as it was written
Given an English lesson whose translations were made from its current text
When I run the translator
Then the translations are unchanged and only the key check reached the model
And it says there is nothing to do

### Scenario: A translation of an older English text is made again
Given a Japanese lesson made from an older version of its English source
When I run the translator
Then it says it retranslates that file because the source changed
And the file now holds a new translation stamped with the current source

### Scenario: An English-only draft is not translated
Given an English lesson marked translate: false
When I run the translator
Then no translation file is written
And it lists the lesson as an English-only draft

### Scenario: Missing text in the YAML files is filled and existing text is kept
Given ui.yaml and resources.yaml with some Japanese and Portuguese text missing
When I run the translator
Then the missing text is filled from the model
And the text that was there is unchanged

### Scenario: A rejected API key stops the run and says what to do
Given a GEMINI_API_KEY the API rejects
When I run the translator
Then it stops with an error that says the key was rejected and how to replace it
And no file is written
