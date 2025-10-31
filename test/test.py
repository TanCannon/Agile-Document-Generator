import subprocess
import sys
from playwright.sync_api import sync_playwright
import os
import pathlib

def ensure_playwright_browsers():
    """Ensure Playwright browsers are installed before use."""
    try:
        with sync_playwright() as p:
            p.chromium.launch()
        # If launch worked, browsers are ready
    except Exception:
        print("Installing Playwright browsers...")
        subprocess.run([sys.executable, "-m", "playwright", "install", "--with-deps"], check=True)
        print("Playwright browsers installed successfully.")

def save_ui_mockup_as_image(html_code: str, output_png: str = "ui_mockup.png"):
    """
    Render UI mockup HTML (e.g., login page, dashboard, tic-tac-toe board)
    and save as PNG.
    """
    ensure_playwright_browsers()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_viewport_size({"width": 1200, "height": 800})

        page.set_content(html_code, wait_until="networkidle")

        # Save screenshot
        page.screenshot(path=output_png)
        print(f"✅ Saved UI mockup as {output_png}")

        browser.close()

def save_workflow_as_image(html_code: str, output_png: str = "workflow.png", output_svg: str = "workflow.svg"):
    """
    Render workflow diagrams (e.g., Mermaid.js) and save as PNG + SVG.
    """
    ensure_playwright_browsers()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_viewport_size({"width": 1200, "height": 800})

        page.set_content(html_code, wait_until="networkidle")

        # Save PNG screenshot
        page.screenshot(path=output_png)

        # Try extracting SVG
        try:
            svg_element = page.locator("svg").first
            if svg_element:
                svg_code = svg_element.evaluate("el => el.outerHTML")
                with open(output_svg, "w", encoding="utf-8") as f:
                    f.write(svg_code)
                print(f"Saved workflow as {output_png} and {output_svg}")
            else:
                print(f"Saved {output_png}, but no SVG found")
        except Exception as e:
            print(f"Saved {output_png}, but SVG export failed: {e}")

        browser.close()

def capture_sections_screenshots(html_path: str, output_dir: str = "screenshots", wait_ms: int = 1000):
    """
    Captures screenshots of all <section id="..."> screens in a single HTML file.

    Args:
        html_path (str): Absolute file URL to the HTML file, e.g., "file:///C:/path/to/app.html"
        output_dir (str): Folder to save screenshots.
        wait_ms (int): Time to wait after navigation to allow rendering (in milliseconds).
    """
    ensure_playwright_browsers()

    os.makedirs(output_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_viewport_size({"width": 1200, "height": 800})
        page.goto(html_path)

        # Extract all <section id="..."> values
        section_ids = page.eval_on_selector_all("section[id]", "els => els.map(e => e.id)")
        print("Sections found:", section_ids)

        for section_id in section_ids:
            page.goto(f"{html_path}#{section_id}")
            page.wait_for_timeout(wait_ms)
            screenshot_path = os.path.join(output_dir, f"{section_id}.png")
            page.screenshot(path=screenshot_path)
            print(f"Saved screenshot: {screenshot_path}")

        browser.close()
if __name__ == "__main__":
    # Example Mermaid workflow diagram
    html_code1 = """
        <html>
        <head>
        <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
        </head>
        <body>
        <div class="mermaid">
            graph TD
            A[User Login] --> B[Dashboard]
            B --> C[Profile Settings]
            B --> D[Reports]
            C --> E[Logout]
            D --> E[Logout]
        </div>
        <script>
            mermaid.initialize({ startOnLoad: true });
        </script>
        </body>
        </html>
    """
   
    # save_ui_mockup_as_image(html_code4, "./test/test-answers/ui-mockups-demo-FRD.png")
    # save_workflow_as_image(html_code3, "workflow.png", "workflow.svg")

    html_file5 = "./test/test-answers/page6.html"
    output_file = "./screenshots/pagetemp"
    # Get absolute path
    abs_path = pathlib.Path(html_file5).resolve()
    # Convert to file URL for Playwright
    file_url = abs_path.as_uri()
    print(f"Capturing screenshots of {file_url}")
    # capture_sections_screenshots("C:/Users/tanmayan/Documents/Project Studies/GAIG/Ollama-practice/test/test-answers/page3.html")
    capture_sections_screenshots(file_url, output_file)
    print(f"Finished caturring screenshots!")