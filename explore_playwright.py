import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://amiunique.org/fingerprint", wait_until="networkidle")

        # # Evaluate navigator.webdriver in the page context
        # is_webdriver = await page.evaluate("navigator.webdriver")
        # print(f"navigator.webdriver: {is_webdriver}")

        try:
            await page.locator("button:has-text('Accept')").click()
            print("Clicked 'Accept' on cookie popup.")
        except Exception as e:
            print("Could not find or click 'Accept':", e)

        await page.screenshot(path="screenshot.png", full_page=True)

        # await asyncio.sleep(9999)
        await browser.close()


asyncio.run(main())
