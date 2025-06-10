#!/usr/bin/env python3
# check-playwright.py
import sys
from playwright.sync_api import sync_playwright, Page, Browser, BrowserType


def run(browser: str, headless: str, script: str, url=None):
    headless = "headless" in headless.lower()
    with sync_playwright() as pw:
        browser_type: BrowserType = getattr(pw, browser)
        browser: Browser = browser_type.launch(headless=headless)
        page: Page = browser.new_page(viewport={"width": 1920, "height": 1080})
        if url:
            page.goto(url)
        result = page.evaluate(script)
        return result


if __name__ == "__main__":
    print(run(*sys.argv[1:]))


# python checkplaywright.py chromium headless "navigator.webdriver" https://example.com
