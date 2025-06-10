import sys
from checkselenium import run as run_selenium
from checkplaywright import run as run_playwright


def run(script: str, url=None):
    data = {}
    for toolkit, tookit_script in [
        ("selenium", run_selenium),
        ("playwright", run_playwright),
    ]:
        for browser in ["chromium", "firefox"]:
            for head in ["headless", "headful"]:
                data[f'{toolkit:<10}:{head:<8}:{browser:<8}:{url or ""}'.strip(":")] = (
                    tookit_script(browser, head, script, url)
                )
    return data


if __name__ == "__main__":
    for query, result in run(*sys.argv[1:]).items():
        print(f"{query}: {result}")


# check secure connections - result should always be "default"
# python checkall.py "Notification.permission" https://httpbin.org/headers

# check unsecure connections - result should be "denied" for chromium and "default" for firefox
#  python checkall.py  "Notification.permission" http://httpbin.org/headers
