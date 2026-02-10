import asyncio
import sys
import os

# পাথ ফিক্স
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.engine.playwright_engine import initiate_verification

async def main():
    test_url = "https://services.sheerid.com/verify/67c8c14f5f17a83b745e3f82/?verificationId="
    user_id = 1864128377 
    
    print("🚀 Starting 200% Manual Test...")
    # এখানে ২টি আর্গুমেন্টই পাঠানো হচ্ছে যা ইঞ্জিনের সাথে এখন সামঞ্জস্যপূর্ণ
    result = await initiate_verification(user_id, test_url)
    print(f"✅ Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())