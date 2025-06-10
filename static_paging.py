# Basics of hhtpx

# 1. httpx.TimeoutExcception error occurs when a request takes longer than the specified/default timeout duration
# httpx.get("https://httpbin.org/delay/10", timeout=httpx.Timeout(60.0))

# 2. httpx.TooManyRedirects: The httpx.TooManyRedirects is raised when a request exceeds the maximum number of allowed redirects.
# response = httpx.get("https://httpbin.dev/redirect/3",allow_redirects=False,)   # disable automatic redirect handling

# 3. httpx.HTTPStatusError: The httpx.HTTPStatusError error is raised when using raise_for_status=True parameter and the server response status code not in the 200-299 range like 404:
# response = httpx.get("https://httpbin.dev/redirect/3",raise_for_status=True,) # When web scraping status codes outside of 200-299 range can mean the scraper is being blocked.


# -------------------------------------------------------------------------------------------------------------------

# import httpx
# from parsel import Selector
# import time

# start_time = time.time()

# base_url = "https://web-scraping.dev/products"

# first_page_response = httpx.get(url=base_url)

# selector = Selector(text=first_page_response.text)

# other_page_urls = set(selector.css(".paging>a::attr(href)").getall())

# all_product_urls = set()

# for page_url in other_page_urls:
#     response = httpx.get(url=page_url)

#     page_selector = Selector(text=response.text)
#     product_urls = set(page_selector.css(".product h3 a::attr(href)").getall())

#     for urls in product_urls:
#         all_product_urls.add(urls)

# end_time = time.time()

# for product_url in all_product_urls:
#     print(product_url)

# print(f"total operation time {end_time - start_time:.3f}s")


# ------------------------------------------------------------- Async ---------------------

import asyncio
import httpx
from parsel import Selector
import time


async def scrape():
    product_urls = []
    start_time = time.time()

    async with httpx.AsyncClient(
        http2=True,
        limits=httpx.Limits(max_connections=10),
        timeout=httpx.Timeout(60.0),
    ) as client:

        first_page_response = await client.get("https://web-scraping.dev/products")
        selector = Selector(text=first_page_response.text)
        other_pages_urls = set(selector.css(".paging>a::attr(href)").getall())

        #  gether() Waits for all tasks to finish before returning. Returns results in the same order as the input tasks.
        # Use case: When you need all results and order matters. You want to process all results at once after everything is done.
        # responses = await asyncio.gather(*[client.get(url) for url in other_pages_urls])  # All responses come together, ordered

        # to scrape urls concurrently we can use asyncio.as_completed or asyncio.gather
        for response in asyncio.as_completed(
            [client.get(url) for url in other_pages_urls]
        ):
            response = await response
            selector = Selector(text=response.text)

            product_urls.extend(selector.css(".product h3 a::attr(href)").getall())

    end_time = time.time()

    print(f"Total producted fetched {len(product_urls)}")
    print(f"Total operation time {end_time-start_time}")


asyncio.run(scrape())
