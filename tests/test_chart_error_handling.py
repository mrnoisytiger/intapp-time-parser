import os
import sys
from playwright.sync_api import sync_playwright, expect

def test_fetch_http_error(page):
    # Load the chart.html file
    file_path = "file://" + os.path.abspath("chart.html")

    # Block external requests to avoid timeouts if internet is restricted
    page.route("https://cdn.jsdelivr.net/**", lambda route: route.fulfill(status=200, body=""))

    page.goto(file_path)

    # Mock the fetch to return a 500 error
    page.route("**/webhook/trello-chart**", lambda route: route.fulfill(
        status=500,
        body="Internal Server Error"
    ))

    # Listen for dialogs (alerts)
    alert_message = []
    page.once("dialog", lambda dialog: (alert_message.append(dialog.message), dialog.dismiss()))

    # Listen for console errors
    console_errors = []
    page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

    # Click the Run Workflow button
    run_button = page.get_by_role("button", name="Run Workflow")
    run_button.click()

    # Wait for the button to be enabled again
    expect(run_button).to_be_enabled(timeout=5000)
    expect(run_button).to_have_text("Run Workflow")

    assert len(alert_message) > 0, "Alert was not shown"
    assert "Failed to connect to n8n workflow" in alert_message[0]
    assert any("HTTP error! status: 500" in err for err in console_errors), f"Expected console error not found in {console_errors}"

def test_fetch_network_error(page):
    # Load the chart.html file
    file_path = "file://" + os.path.abspath("chart.html")

    # Block external requests
    page.route("https://cdn.jsdelivr.net/**", lambda route: route.fulfill(status=200, body=""))

    page.goto(file_path)

    # Mock the fetch to fail
    page.route("**/webhook/trello-chart**", lambda route: route.abort("failed"))

    # Listen for dialogs (alerts)
    alert_message = []
    page.once("dialog", lambda dialog: (alert_message.append(dialog.message), dialog.dismiss()))

    # Listen for console errors
    console_errors = []
    # Clear existing console listeners if any (though we use a new page now in refined runner)
    page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

    # Click the Run Workflow button
    run_button = page.get_by_role("button", name="Run Workflow")
    run_button.click()

    # Wait for the button to be enabled again
    expect(run_button).to_be_enabled(timeout=5000)
    expect(run_button).to_have_text("Run Workflow")

    assert len(alert_message) > 0, "Alert was not shown"
    assert "Failed to connect to n8n workflow" in alert_message[0]
    assert any("Error fetching from n8n" in err for err in console_errors), f"Expected console error not found in {console_errors}"

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        try:
            print("Running test_fetch_http_error...")
            context1 = browser.new_context()
            page1 = context1.new_page()
            test_fetch_http_error(page1)
            context1.close()
            print("test_fetch_http_error passed!")

            print("Running test_fetch_network_error...")
            context2 = browser.new_context()
            page2 = context2.new_page()
            test_fetch_network_error(page2)
            context2.close()
            print("test_fetch_network_error passed!")
        except Exception as e:
            print(f"Test failed: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
        finally:
            browser.close()
