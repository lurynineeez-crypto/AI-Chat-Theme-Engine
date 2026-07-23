import os
from pathlib import Path

from playwright.sync_api import Locator, Page, expect, sync_playwright


BASE_URL = os.environ.get("HOST_UI_BASE_URL", "http://127.0.0.1:4173")
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "validation"


def app_url(*, dev: bool = False) -> str:
    return f"{BASE_URL}/?dev=1" if dev else BASE_URL


def assert_no_page_overflow(page: Page) -> None:
    metrics = page.evaluate(
        """() => ({
            documentScrollHeight: document.documentElement.scrollHeight,
            documentClientHeight: document.documentElement.clientHeight,
            documentScrollWidth: document.documentElement.scrollWidth,
            documentClientWidth: document.documentElement.clientWidth,
            bodyScrollHeight: document.body.scrollHeight,
            bodyClientHeight: document.body.clientHeight,
            windowScrollX: window.scrollX,
            windowScrollY: window.scrollY,
        })"""
    )
    assert metrics["documentScrollHeight"] <= metrics["documentClientHeight"]
    assert metrics["bodyScrollHeight"] <= metrics["bodyClientHeight"]
    assert metrics["documentScrollWidth"] <= metrics["documentClientWidth"]
    assert metrics["windowScrollX"] == 0
    assert metrics["windowScrollY"] == 0


def assert_minimum_touch_target(locator: Locator) -> None:
    box = locator.bounding_box()
    assert box is not None
    assert box["width"] >= 44
    assert box["height"] >= 44


def open_app(page: Page, *, dev: bool = False) -> None:
    page.goto(app_url(dev=dev))
    page.wait_for_load_state("networkidle")
    expect(page.locator("#conversation-title")).to_have_text("Host UI structure review")
    assert page.locator("#app #dev-harness").count() == 0
    assert page.locator("#dev-harness").evaluate(
        "(el) => el.parentElement === document.body"
    )
    if dev:
        expect(page.locator("#dev-harness")).to_be_visible()
    else:
        expect(page.locator("#dev-harness")).to_be_hidden()
        expect(page.locator("#app")).not_to_have_attribute(
            "data-validation-decoration", ""
        )
    expect(page.locator("#chat-content")).not_to_have_attribute("aria-live", "")
    live_region = page.locator("#host-status-live-region")
    expect(live_region).to_have_attribute("aria-live", "polite")
    expect(live_region).to_have_attribute("aria-atomic", "true")
    assert page.locator("[aria-live]").count() == 1
    assert_no_page_overflow(page)


def assert_product_controls(page: Page, *, mobile: bool) -> None:
    if mobile:
        sidebar = page.locator("#mobile-drawer")
        controls = [
            page.get_by_role("button", name="Open conversation sidebar"),
            sidebar.get_by_role("button", name="Close conversation sidebar"),
            sidebar.get_by_role("button", name="New chat"),
            sidebar.get_by_role("button", name="Account and settings unavailable"),
            page.get_by_role("button", name="More conversation actions unavailable"),
            page.get_by_role("button", name="Send"),
        ]
    else:
        sidebar = page.locator(".sidebar--desktop")
        controls = [
            sidebar.get_by_role("button", name="New chat"),
            sidebar.get_by_role("button", name="Account and settings unavailable"),
            page.get_by_role("button", name="More conversation actions unavailable"),
            page.get_by_role("button", name="Send"),
        ]

    for control in controls:
        expect(control).to_be_visible()
        assert control.evaluate("(el) => el.tagName") == "BUTTON"
        if "unavailable" in (control.get_attribute("aria-label") or ""):
            expect(control).to_be_disabled()
            expect(control).to_have_attribute("aria-disabled", "true")
        if mobile:
            assert_minimum_touch_target(control)


def validate_desktop_layout(page: Page, width: int, screenshot_name: str) -> None:
    page.set_viewport_size({"width": width, "height": 900})
    open_app(page)

    expect(page.locator(".sidebar--desktop")).to_be_visible()
    expect(page.locator("#open-drawer")).to_be_hidden()
    assert_product_controls(page, mobile=False)
    assert_decoration_stack(page.locator(".sidebar--desktop"), 0)
    assert_decoration_stack(
        page.locator(".sidebar--desktop .brand-area"), 8
    )
    assert_decoration_stack(page.locator(".chat-header"), 8)
    assert_decoration_stack(page.locator("#composer"), 8)

    conversation_list = page.locator(".sidebar--desktop .conversation-list")
    list_metrics = conversation_list.evaluate(
        "(el) => ({scrollHeight: el.scrollHeight, clientHeight: el.clientHeight})"
    )
    assert list_metrics["scrollHeight"] > list_metrics["clientHeight"]
    conversation_list.evaluate("(el) => { el.scrollTop = 120; }")
    assert conversation_list.evaluate("(el) => el.scrollTop") > 0
    conversation_list.evaluate("(el) => { el.scrollTop = 0; }")
    assert_no_page_overflow(page)
    page.screenshot(path=str(OUTPUT_DIR / screenshot_name), full_page=False)


def validate_long_conversation_and_local_interactions(page: Page) -> None:
    page.set_viewport_size({"width": 1200, "height": 900})
    open_app(page)
    page.locator('.sidebar--desktop [data-conversation-id="long"]').click()
    expect(page.locator("#conversation-title")).to_contain_text(
        "An intentionally very long conversation title"
    )

    viewport = page.locator("#message-viewport")
    viewport_metrics = viewport.evaluate(
        """(el) => ({
            scrollHeight: el.scrollHeight,
            clientHeight: el.clientHeight,
            scrollWidth: el.scrollWidth,
            clientWidth: el.clientWidth,
        })"""
    )
    assert viewport_metrics["scrollHeight"] > viewport_metrics["clientHeight"]
    assert viewport_metrics["scrollWidth"] <= viewport_metrics["clientWidth"]

    header_before = page.locator(".chat-header").bounding_box()
    composer_before = page.locator("#composer").bounding_box()
    viewport.evaluate("(el) => { el.scrollTop = el.scrollHeight / 2; }")
    page.wait_for_timeout(50)
    assert viewport.evaluate("(el) => el.scrollTop") > 0
    assert page.locator(".chat-header").bounding_box() == header_before
    assert page.locator("#composer").bounding_box() == composer_before
    assert_no_page_overflow(page)
    page.screenshot(
        path=str(OUTPUT_DIR / "long-conversation-scrolled-1200x900.png"),
        full_page=False,
    )

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
    expect(page.locator("#host-status-live-region")).to_have_text("Message sent.")
    assert "Follow the bottom" not in page.locator(
        "#host-status-live-region"
    ).text_content()
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

    page.locator(".sidebar--desktop [data-action='new-chat']").click()
    expect(page.get_by_role("heading", name="Start a local conversation")).to_be_visible()
    expect(editor).to_be_focused()

    search = page.locator(".sidebar--desktop [data-role='conversation-search']")
    search.fill("no title can match this value")
    expect(
        page.locator(".sidebar--desktop .conversation-list-empty")
    ).to_have_text("No matching conversations")
    search.fill("")


def capture_fixture(page: Page, fixture: str, screenshot_name: str) -> None:
    harness = page.locator("#dev-harness")
    harness.locator("#demo-state").select_option(fixture)

    if fixture == "empty":
        expect(
            page.get_by_role("heading", name="Start a local conversation")
        ).to_be_visible()
        assert_decoration_stack(page.locator(".empty-state"), 12)
    elif fixture == "loading":
        expect(page.locator('[data-component="loading-state"]')).to_contain_text(
            "Loading conversation"
        )
        expect(page.locator("#message-input")).to_be_disabled()
        expect(page.locator("#host-status-live-region")).to_have_text(
            "Conversation loading."
        )
    elif fixture == "error":
        expect(page.get_by_role("alert")).to_contain_text(
            "Conversation could not be shown"
        )
        expect(page.locator("#host-status-live-region")).to_have_text(
            "Conversation failed to load."
        )

    harness.evaluate("(el) => { el.hidden = true; }")
    page.screenshot(path=str(OUTPUT_DIR / screenshot_name), full_page=False)
    harness.evaluate("(el) => { el.hidden = false; }")


def validate_development_harness_and_states(page: Page) -> None:
    page.set_viewport_size({"width": 1440, "height": 900})
    open_app(page, dev=True)
    harness = page.locator("#dev-harness")
    expect(harness).to_have_attribute("data-component", "development-harness")
    assert page.locator(".chat-header #demo-state").count() == 0
    assert page.locator(".chat-header #appearance-toggle").count() == 0

    appearance_toggle = harness.locator("#appearance-toggle")
    expect(appearance_toggle).to_have_attribute(
        "aria-label", "Use dark neutral QA appearance"
    )
    appearance_toggle.click()
    expect(page.locator("#app")).to_have_attribute("data-appearance", "dark")
    appearance_toggle.click()
    expect(page.locator("#app")).to_have_attribute("data-appearance", "light")

    capture_fixture(page, "empty", "state-empty-1440x900.png")
    capture_fixture(page, "loading", "state-loading-1440x900.png")
    capture_fixture(page, "error", "state-error-1440x900.png")

    harness.locator("#demo-state").select_option("disabled")
    expect(page.locator("#message-input")).to_be_disabled()
    expect(page.locator("#send-button")).to_be_disabled()

    harness.locator("#demo-state").select_option("error")
    page.get_by_role("button", name="Try again").click()
    expect(page.locator("#message-input")).to_be_enabled()
    expect(harness.locator("#demo-state")).to_have_value("conversation")
    assert_no_page_overflow(page)


def assert_decoration_stack(component: Locator, expected_overflow: float) -> None:
    stack = component.evaluate(
        """(el) => {
            const outside = el.querySelector(':scope > .decoration-boundary--outside');
            const inside = el.querySelector(':scope > .decoration-boundary--inside');
            const content = el.querySelector(':scope > .content-layer');
            const outsideSlot = outside.querySelector('.decoration-slot');
            const insideSlot = inside.querySelector('.decoration-slot');
            const rect = (node) => {
                const value = node.getBoundingClientRect();
                return {
                    left: value.left,
                    top: value.top,
                    right: value.right,
                    bottom: value.bottom,
                    width: value.width,
                    height: value.height,
                };
            };
            return {
                component: rect(el),
                outside: rect(outside),
                inside: rect(inside),
                outsideZ: Number(getComputedStyle(outside).zIndex),
                insideZ: Number(getComputedStyle(inside).zIndex),
                contentZ: Number(getComputedStyle(content).zIndex),
                outsideOverflow: getComputedStyle(outside).overflow,
                insideOverflow: getComputedStyle(inside).overflow,
                outsidePointer: getComputedStyle(outside).pointerEvents,
                insidePointer: getComputedStyle(inside).pointerEvents,
                outsideSlotPointer: getComputedStyle(outsideSlot).pointerEvents,
                insideSlotPointer: getComputedStyle(insideSlot).pointerEvents,
                outsideHidden: outside.getAttribute('aria-hidden'),
                insideHidden: inside.getAttribute('aria-hidden'),
                outsideSlotHidden: outsideSlot.getAttribute('aria-hidden'),
                insideSlotHidden: insideSlot.getAttribute('aria-hidden'),
            };
        }"""
    )
    assert stack["contentZ"] > stack["insideZ"] > stack["outsideZ"]
    assert stack["insideOverflow"] == "hidden"
    assert stack["outsideOverflow"] == "hidden"
    assert stack["outsidePointer"] == "none"
    assert stack["insidePointer"] == "none"
    assert stack["outsideSlotPointer"] == "none"
    assert stack["insideSlotPointer"] == "none"
    assert stack["outsideHidden"] == "true"
    assert stack["insideHidden"] == "true"
    assert stack["outsideSlotHidden"] == "true"
    assert stack["insideSlotHidden"] == "true"

    component_rect = stack["component"]
    inside_rect = stack["inside"]
    outside_rect = stack["outside"]
    assert abs(inside_rect["width"] - component_rect["width"]) <= 2
    assert abs(inside_rect["height"] - component_rect["height"]) <= 2
    assert inside_rect["left"] >= component_rect["left"]
    assert inside_rect["top"] >= component_rect["top"]
    assert inside_rect["right"] <= component_rect["right"]
    assert inside_rect["bottom"] <= component_rect["bottom"]
    assert abs(component_rect["left"] - outside_rect["left"] - expected_overflow) <= 2
    assert abs(component_rect["top"] - outside_rect["top"] - expected_overflow) <= 2
    assert abs(outside_rect["right"] - component_rect["right"] - expected_overflow) <= 2
    assert abs(outside_rect["bottom"] - component_rect["bottom"] - expected_overflow) <= 2


def assert_marker_does_not_receive_pointer(page: Page, marker: Locator) -> None:
    box = marker.bounding_box()
    assert box is not None
    point = {"x": box["x"] + box["width"] / 2, "y": box["y"] + box["height"] / 2}
    hit_classes = page.evaluate(
        """({x, y}) => {
            const hit = document.elementFromPoint(x, y);
            return hit ? hit.className : '';
        }""",
        point,
    )
    assert "decoration-slot" not in str(hit_classes)
    assert "decoration-boundary" not in str(hit_classes)


def validate_decoration_contract(page: Page) -> None:
    page.set_viewport_size({"width": 1200, "height": 900})
    open_app(page)
    production_sizes = {
        "incoming": page.locator('[data-component="incoming-message"]').first.bounding_box(),
        "outgoing": page.locator('[data-component="outgoing-message"]').first.bounding_box(),
        "avatar": page.locator(".avatar-frame").first.bounding_box(),
    }

    fixtures = [
        (
            "bubble-inside",
            page.locator('[data-component="incoming-message"]').first,
            '[data-theme-hook="incoming-bubble-decoration-inside"]',
            "incoming",
            12,
            "decoration-bubble-inside-1200x900.png",
        ),
        (
            "bubble-outside",
            page.locator('[data-component="outgoing-message"]').first,
            '[data-theme-hook="outgoing-bubble-decoration-outside"]',
            "outgoing",
            12,
            "decoration-bubble-outside-1200x900.png",
        ),
        (
            "avatar-outside",
            page.locator(".avatar-frame").first,
            '[data-theme-hook="avatar-frame-decoration-outside"]',
            "avatar",
            8,
            "decoration-avatar-outside-1200x900.png",
        ),
    ]

    for fixture, component, marker_selector, size_key, overflow, screenshot in fixtures:
        page.goto(f"{BASE_URL}/?dev=1&decorations={fixture}")
        page.wait_for_load_state("networkidle")
        expect(page.locator("#app")).to_have_attribute(
            "data-validation-decoration", fixture
        )
        page.locator("#dev-harness").evaluate("(el) => { el.hidden = true; }")
        component = (
            page.locator(".avatar-frame").first
            if size_key == "avatar"
            else page.locator(
                f'[data-component="{size_key}-message"]'
            ).first
        )
        assert_decoration_stack(component, overflow)

        fixture_box = component.bounding_box()
        baseline_box = production_sizes[size_key]
        assert fixture_box is not None and baseline_box is not None
        assert abs(fixture_box["width"] - baseline_box["width"]) <= 1
        assert abs(fixture_box["height"] - baseline_box["height"]) <= 1

        marker = component.locator(marker_selector)
        expect(marker).to_be_visible()
        assert_marker_does_not_receive_pointer(page, marker)

        marker_box = marker.bounding_box()
        assert marker_box is not None
        if fixture == "bubble-inside":
            assert marker_box["x"] >= fixture_box["x"]
            assert marker_box["y"] >= fixture_box["y"]
            assert marker_box["x"] + marker_box["width"] <= (
                fixture_box["x"] + fixture_box["width"]
            )
            assert marker_box["y"] + marker_box["height"] <= (
                fixture_box["y"] + fixture_box["height"]
            )
        else:
            extends_outside = (
                marker_box["x"] < fixture_box["x"]
                or marker_box["y"] < fixture_box["y"]
                or marker_box["x"] + marker_box["width"]
                > fixture_box["x"] + fixture_box["width"]
                or marker_box["y"] + marker_box["height"]
                > fixture_box["y"] + fixture_box["height"]
            )
            assert extends_outside

        assert_no_page_overflow(page)
        page.screenshot(path=str(OUTPUT_DIR / screenshot), full_page=False)

    page.goto(BASE_URL)
    page.wait_for_load_state("networkidle")
    expect(page.locator("#app")).not_to_have_attribute(
        "data-validation-decoration", ""
    )


def validate_mobile(page: Page) -> None:
    page.set_viewport_size({"width": 390, "height": 844})
    open_app(page)
    expect(page.locator(".sidebar--desktop")).to_be_hidden()
    expect(page.locator("#open-drawer")).to_be_visible()
    assert_no_page_overflow(page)
    page.screenshot(
        path=str(OUTPUT_DIR / "mobile-390x844-drawer-closed.png"),
        full_page=False,
    )

    opener = page.get_by_role("button", name="Open conversation sidebar")
    opener.focus()
    opener.press("Enter")
    expect(page.locator("#mobile-drawer")).to_have_attribute("aria-hidden", "false")
    expect(page.get_by_role("button", name="Close conversation sidebar")).to_be_focused()
    assert_product_controls(page, mobile=True)

    last_conversation = page.locator(
        '#mobile-drawer [data-role="conversation-list"] [data-conversation-id]'
    ).last
    last_conversation.focus()
    last_conversation.press("Tab")
    expect(page.get_by_role("button", name="Close conversation sidebar")).to_be_focused()

    page.wait_for_timeout(250)
    drawer_box = page.locator("#mobile-drawer").bounding_box()
    assert drawer_box is not None and abs(drawer_box["x"]) <= 1
    page.screenshot(
        path=str(OUTPUT_DIR / "mobile-390x844-drawer-open.png"),
        full_page=False,
    )

    page.get_by_role("button", name="Close conversation sidebar").click()
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
    assert_no_page_overflow(page)


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
        page.on("pageerror", lambda error: console_errors.append(str(error)))

        validate_desktop_layout(
            page, 1440, "desktop-1440x900-conversation.png"
        )
        validate_desktop_layout(
            page, 1200, "desktop-1200x900-conversation.png"
        )
        validate_long_conversation_and_local_interactions(page)
        validate_development_harness_and_states(page)
        validate_decoration_contract(page)
        validate_mobile(page)

        browser.close()

    assert not console_errors, f"Browser console errors: {console_errors}"
    print("HOST_UI_BASELINE_VALIDATION_OK")


if __name__ == "__main__":
    main()
