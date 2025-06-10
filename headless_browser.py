import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        # Launch Chromium with devtools (this opens Chrome with inspect panel)
        browser = await p.chromium.launch(headless=False, devtools=True)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://example.com")

        # Evaluate navigator.webdriver in the page context
        is_webdriver = await page.evaluate("navigator.webdriver")
        print(f"navigator.webdriver: {is_webdriver}")

        # Keep browser open for inspection
        print("Browser is open with DevTools. Press Ctrl+C to exit.")
        await asyncio.sleep(9999)


asyncio.run(main())
