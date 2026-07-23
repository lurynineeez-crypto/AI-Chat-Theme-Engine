import os
from pathlib import Path

from playwright.sync_api import Page, expect, sync_playwright


BASE_URL = os.environ.get("HOST_UI_BASE_URL", "http://127.0.0.1:4173")
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "validation"


def assert_no_page_overflow(page: Page) -> None:
    metrics = page.evaluate(
        """() => ({
            documentScrollHeight: document.documentElement.scrollHeight,
            documentClientHeight: document.documentElement.clientHeight,
            documentScrollWidth: document.documentElement.scrollWidth,
            documentClientWidth: document.documentElement.clientWidth,
            bodyScrollHeight: document.body.scrollHeight,
            bodyClientHeight: document.body.clientHeight,
        })"""
    )
    assert metrics["documentScrollHeight"] <= metrics["documentClientHeight"]
    assert metrics["bodyScrollHeight"] <= metrics["bodyClientHeight"]
    assert metrics["documentScrollWidth"] <= metrics["documentClientWidth"]


def open_app(page: Page) -> None:
    page.goto(BASE_URL)
    page.wait_for_load_state("networkidle")
    expect(page.locator("#conversation-title")).to_have_text("Host UI structure review")
    assert_no_page_overflow(page)


def validate_desktop(page: Page, width: int, screenshot_name: str) -> None:
    page.set_viewport_size({"width": width, "height": 900})
    open_app(page)

    expect(page.locator(".sidebar--desktop")).to_be_visible()
    expect(page.locator("#open-drawer")).to_be_hidden()
    appearance_toggle = page.locator("#appearance-toggle")
    appearance_toggle.click()
    expect(page.locator("#app")).to_have_attribute("data-appearance", "dark")
    appearance_toggle.click()
    expect(page.locator("#app")).to_have_attribute("data-appearance", "light")
    list_metrics = page.locator(".sidebar--desktop .conversation-list").evaluate(
        "(el) => ({scrollHeight: el.scrollHeight, clientHeight: el.clientHeight})"
    )
    assert list_metrics["scrollHeight"] > list_metrics["clientHeight"]

    page.locator('.sidebar--desktop [data-conversation-id="long"]').click()
    expect(page.locator("#conversation-title")).to_contain_text(
        "An intentionally very long conversation title"
    )
    viewport = page.locator("#message-viewport")
    overflow_metrics = viewport.evaluate(
        "(el) => ({scrollWidth: el.scrollWidth, clientWidth: el.clientWidth})"
    )
    assert overflow_metrics["scrollWidth"] <= overflow_metrics["clientWidth"]

    viewport.evaluate("(el) => { el.scrollTop = 160; }")
    old_top = viewport.evaluate("(el) => el.scrollTop")
    page.locator("#message-input").fill("Reading position preservation check")
    page.locator("#send-button").click()
    page.wait_for_timeout(50)
    new_top = viewport.evaluate("(el) => el.scrollTop")
    assert abs(new_top - old_top) <= 2
    expect(
        page.locator(
            '.sidebar--desktop [data-conversation-id="long"] .conversation-preview'
        )
    ).to_have_text("Reading position preservation check")

    viewport.evaluate("(el) => { el.scrollTop = el.scrollHeight; }")
    page.locator("#message-input").fill("Follow the bottom after sending")
    page.locator("#message-input").press("Enter")
    page.wait_for_timeout(50)
    bottom_distance = viewport.evaluate(
        "(el) => el.scrollHeight - el.scrollTop - el.clientHeight"
    )
    assert bottom_distance <= 2

    editor = page.locator("#message-input")
    editor.fill("Line one")
    editor.press("Shift+Enter")
    editor.type("Line two")
    assert editor.input_value() == "Line one\nLine two"

    editor.fill("\n".join(f"Line {index}" for index in range(18)))
    editor_box = editor.bounding_box()
    assert editor_box is not None
    assert 44 <= editor_box["height"] <= 161
    assert editor.evaluate("(el) => getComputedStyle(el).overflowY") == "auto"
    editor.fill("")

    state_select = page.locator("#demo-state")
    state_select.select_option("empty")
    expect(page.get_by_role("heading", name="Start a local conversation")).to_be_visible()
    state_select.select_option("loading")
    expect(page.locator('[data-component="loading-state"]')).to_contain_text(
        "Loading conversation"
    )
    expect(editor).to_be_disabled()
    state_select.select_option("error")
    expect(page.get_by_role("alert")).to_contain_text(
        "Conversation could not be shown"
    )
    page.get_by_role("button", name="Try again").click()
    expect(editor).to_be_enabled()
    state_select.select_option("disabled")
    expect(editor).to_be_disabled()
    expect(page.locator("#send-button")).to_be_disabled()
    state_select.select_option("conversation")

    page.locator(".sidebar--desktop [data-action='new-chat']").click()
    expect(page.get_by_role("heading", name="Start a local conversation")).to_be_visible()
    expect(editor).to_be_focused()

    search = page.locator(".sidebar--desktop [data-role='conversation-search']")
    search.fill("no title can match this value")
    expect(
        page.locator(".sidebar--desktop .conversation-list-empty")
    ).to_have_text("No matching conversations")
    search.fill("")
    page.locator('.sidebar--desktop [data-conversation-id="welcome"]').click()
    expect(page.locator("#conversation-title")).to_have_text("Host UI structure review")

    assert_no_page_overflow(page)
    page.screenshot(path=str(OUTPUT_DIR / screenshot_name), full_page=False)


def validate_mobile(page: Page) -> None:
    page.set_viewport_size({"width": 390, "height": 844})
    open_app(page)

    expect(page.locator(".sidebar--desktop")).to_be_hidden()
    opener = page.locator("#open-drawer")
    expect(opener).to_be_visible()
    opener.focus()
    opener.press("Enter")
    expect(page.locator("#mobile-drawer")).to_have_attribute("aria-hidden", "false")
    expect(page.locator(".drawer-close")).to_be_focused()

    touch_targets = page.locator(
        "#mobile-drawer button:visible, #mobile-drawer input:visible, "
        "#open-drawer:visible, #send-button:visible"
    )
    for index in range(touch_targets.count()):
        box = touch_targets.nth(index).bounding_box()
        assert box is not None
        assert box["height"] >= 44

    settings = page.locator("#mobile-drawer .settings-button")
    settings.focus()
    settings.press("Tab")
    expect(page.locator(".drawer-close")).to_be_focused()

    page.locator(".drawer-close").click()
    expect(opener).to_be_focused()

    opener.click()
    page.locator("#drawer-backdrop").click(position={"x": 380, "y": 420})
    expect(page.locator("#mobile-drawer")).to_have_attribute("aria-hidden", "true")
    expect(opener).to_be_focused()

    opener.click()
    page.keyboard.press("Escape")
    expect(page.locator("#mobile-drawer")).to_have_attribute("aria-hidden", "true")
    expect(opener).to_be_focused()

    page.emulate_media(reduced_motion="reduce")
    reduced_transition = page.locator("#mobile-drawer").evaluate(
        "(el) => getComputedStyle(el).transitionDuration"
    )
    durations = [
        float(value.strip().removesuffix("s"))
        for value in reduced_transition.split(",")
    ]
    assert all(duration <= 0.001 for duration in durations)

    page.emulate_media(reduced_motion="no-preference")
    opener.click()
    expect(page.locator("#mobile-drawer")).to_have_attribute("aria-hidden", "false")
    expect(page.locator("#mobile-drawer")).to_be_visible()
    page.wait_for_timeout(250)
    drawer_box = page.locator("#mobile-drawer").bounding_box()
    assert drawer_box is not None and abs(drawer_box["x"]) <= 1
    assert_no_page_overflow(page)
    page.screenshot(path=str(OUTPUT_DIR / "mobile-390x844.png"), full_page=False)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    console_errors: list[str] = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        page.on(
            "console",
            lambda message: console_errors.append(message.text)
            if message.type == "error"
            else None,
        )
        page.on(
            "pageerror",
            lambda error: console_errors.append(str(error)),
        )

        validate_desktop(page, 1440, "desktop-1440x900.png")
        validate_desktop(page, 1200, "desktop-1200x900.png")
        validate_mobile(page)

        browser.close()

    assert not console_errors, f"Browser console errors: {console_errors}"
    print("HOST_UI_VALIDATION_OK")


if __name__ == "__main__":
    main()
