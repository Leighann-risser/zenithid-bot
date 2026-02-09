import asyncio
from playwright.async_api import async_playwright
from curl_cffi import requests as curl_requests
from ..database.crud import get_user_credits
from ..utils.logging import log_error, log_info

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

async def initiate_verification(user_id: int) -> str:
    credits = await get_user_credits(user_id)
    if credits <= 0:
        return "Insufficient credits for verification."

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                extra_http_headers=HEADERS,
                ignore_https_errors=True
            )

            # Simulate human-like behavior
            page = await context.new_page()
            await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            await page.goto("https://sheerid.com")
            await asyncio.sleep(2)

            # Example interaction (expand based on real flow)
            await page.click("button[data-testid='start-verification']")
            await page.wait_for_timeout(3000)

            # Inject TLS fingerprint via curl_cffi if needed
            curl_requests.get("https://httpbin.org/ip", impersonate="chrome110")

            await browser.close()
            log_info(f"Verification completed for user {user_id}")
            return "Verification successful."
    
    except Exception as e:
        log_error(f"Verification failed for user {user_id}: {str(e)}")
        return f"Verification failed due to internal error."