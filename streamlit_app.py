import requests
from time import time
import streamlit as st
import asyncio
from playwright.async_api import async_playwright

"""
\## Web scraping on Streamlit Cloud with Playwright

\[!\[Source\](https://img.shields.io/badge/View-Source-<COLOR>.svg)\](https://github.com/your-repo/streamlit-playwright/)

This is a minimal, reproducible example of how to scrape the web with Playwright on Streamlit's Community Cloud.

Fork this repo, and edit `/streamlit_app.py` to customize this app to your heart's desire. :heart:
"""

with st.echo():

    @st.cache_resource
    def get_browser():
        playwright = asyncio.get_event_loop().run_until_complete(async_playwright().start())
        browser = asyncio.get_event_loop().run_until_complete(playwright.chromium.launch())
        return browser

    browser = get_browser()

    @st.cache_data
    async def ExtrayendoHTML(Url: str, browser=browser):
        response = requests.get(Url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            result = 'Using BeautifulSoup'
            print('\033[1;32m' + result + '\033[0m')
            return result, response.text

        else:
            result = 'Using Playwright'
            print('\033[1;33m' + result + '\033[0m')

            page = await browser.new_page()

            # Load the webpage
            await page.goto(Url)

            # Wait for the page to fully load
            await page.wait_for_load_state("domcontentloaded")

            # Get the HTML content directly from the browser's DOM
            html_code = await page.content()

            # Get the status code using requests library
            response = requests.get(page.url)

            # Validate the status code
            if response.status_code == 200:
                result = result + ": " + "HTML code extracted successfully"
                print(result)
                await page.close()
                return result, html_code
            else:
                result = result + ": " + "Failed to extract HTML code"
                print(result)
                await page.close()
                return result, html_code

    async def main():
        if url := st.text_input(label="put the url that you want you extract the html code", value="http://example.com", max_chars=100, help="test"):
            start_time = time()
            result, html = await ExtrayendoHTML(Url=url)
            st.markdown(result)
            st.code(html)
            elapsed_time = time() - start_time
            st.markdown(f"### for the extraction of the html code is loaded in {elapsed_time:.2f} seconds")

    asyncio.run(main())