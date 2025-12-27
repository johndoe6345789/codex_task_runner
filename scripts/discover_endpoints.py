"""Discover Codex API endpoints by intercepting browser traffic."""
import asyncio
import json
import os
from pathlib import Path
from playwright.async_api import async_playwright
from dotenv import load_dotenv


def load_cookies_from_env():
    """Load cookies from .env file."""
    load_dotenv(Path(__file__).parent.parent / ".env")
    cookie_str = os.getenv("COOKIE", "")
    
    cookies = []
    for part in cookie_str.split(";"):
        part = part.strip()
        if "=" in part:
            name, value = part.split("=", 1)
            name = name.strip()
            value = value.strip()
            if name and value:
                cookies.append({
                    "name": name,
                    "value": value,
                    "domain": "chatgpt.com",
                    "path": "/",
                    "secure": True,
                    "httpOnly": False,
                    "sameSite": "Lax",
                })
    return cookies


async def discover_endpoints(output_file: str = "discovered_endpoints.json"):
    """Open Codex Cloud and log all API requests."""
    endpoints = []
    
    cookies = load_cookies_from_env()
    if not cookies:
        print("Warning: No cookies found in .env")
    else:
        print(f"Loaded {len(cookies)} cookies from .env")
    
    async with async_playwright() as p:
        # Launch browser (not headless so user can interact)
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        
        # Add cookies before navigating
        if cookies:
            await context.add_cookies(cookies)
        
        page = await context.new_page()
        
        # Intercept all requests
        def log_request(request):
            url = request.url
            if "backend-api" in url or "wham" in url or "api" in url.lower():
                entry = {
                    "method": request.method,
                    "url": url,
                }
                # Try to get POST body
                if request.method == "POST":
                    try:
                        entry["body"] = request.post_data
                    except:
                        pass
                endpoints.append(entry)
                print(f"{request.method} {url}")
        
        page.on("request", log_request)
        
        # Navigate to Codex Cloud
        print("Opening Codex Cloud - log in and interact with the UI to discover endpoints")
        print("Press Ctrl+C in terminal when done\n")
        
        try:
            await page.goto("https://chatgpt.com/codex/", wait_until="domcontentloaded", timeout=60000)
        except Exception as e:
            print(f"Navigation: {e}")
        
        # Keep running until user stops or browser closes
        try:
            while True:
                await asyncio.sleep(1)
                # Check if browser is still open
                if not browser.is_connected():
                    break
        except (KeyboardInterrupt, Exception):
            pass
        
        try:
            await browser.close()
        except:
            pass
    
    # Save discovered endpoints
    if endpoints:
        output = Path(output_file)
        output.write_text(json.dumps(endpoints, indent=2))
        print(f"\nSaved {len(endpoints)} endpoints to {output_file}")
        
        # Print unique endpoints
        unique = set()
        for e in endpoints:
            url = e["url"]
            if "backend-api" in url:
                path = url.split("backend-api")[1].split("?")[0]
                unique.add(f"{e['method']} /backend-api{path}")
        
        print("\nUnique endpoints:")
        for ep in sorted(unique):
            print(f"  {ep}")
    else:
        print("\nNo endpoints captured")


if __name__ == "__main__":
    asyncio.run(discover_endpoints())
