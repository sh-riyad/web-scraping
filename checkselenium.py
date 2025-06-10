#!/usr/bin/env python3
# check-selenium.py
import sys
from selenium import webdriver


def run(browser: str, headless: str, script: str, url=None):
    headless = headless.lower()
    if browser == "chromium":
        browser = "chrome"
    if browser == "chrome":
        from selenium.webdriver.chrome.options import Options
    if browser == "firefox":
        from selenium.webdriver.firefox.options import Options
    options = Options()
    if "headless" in headless:
        options.headless = True
    browser = getattr(webdriver, browser.title())(options=options)
    if url:
        browser.get(url)
    result = browser.execute_script(f"return {script}")
    browser.close()
    return result


if __name__ == "__main__":
    print(run(*sys.argv[1:]))


# python checkselenium.py chromium headless "navigator.webdriver" https://example.com
