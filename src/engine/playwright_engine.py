import asyncio
from playwright.async_api import async_playwright
from curl_cffi import requests as curl_requests
# ডাটাবেস সেশন ইমপোর্ট করা হয়েছে যদি প্রয়োজন হয়
from ..database.crud import get_user_credits
from ..utils.logging import log_error, log_info

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

# এখানে target_url যুক্ত করা হয়েছে যা handlers.py থেকে আসে
async def initiate_verification(user_id: int, target_url: str) -> str:
    try:
        # টেস্টের সুবিধার জন্য এবং ডাটাবেস এরর এড়াতে try-except ব্যবহার
        try:
            credits = await get_user_credits(user_id)
            if credits <= 0:
                return "Insufficient credits for verification."
        except Exception as db_err:
            log_error(f"Database error: {db_err}. Proceeding for Admin/Test.")

        async with async_playwright() as p:
            # পিসিতে টেস্টের জন্য headless=False করতে পারেন, সার্ভারে True থাকবে
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                extra_http_headers=HEADERS,
                ignore_https_errors=True
            )

            page = await context.new_page()
            # ডিটেকশন বাইপাস স্ক্রিপ্ট
            await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            # সরাসরি ইউজার প্রদত্ত ইউআরএল-এ যাওয়া
            log_info(f"Navigating to: {target_url}")
            await page.goto(target_url, wait_until="networkidle")
            await asyncio.sleep(3)

            # এখানে আপনার আসল বাইপাস লজিক কাজ করবে
            # উদাহরণ: পেজ টাইটেল চেক করা
            page_title = await page.title()
            
            # TLS Fingerprint impersonation
            curl_requests.get(target_url, impersonate="chrome110")

            await browser.close()
            log_info(f"Verification process finished for user {user_id}")
            return f"Process finished on page: {page_title}"
    
    except Exception as e:
        log_error(f"Verification failed: {str(e)}")
        return f"Error: {str(e)}"