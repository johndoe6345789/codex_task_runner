#!/usr/bin/env python3
"""Compatibility shim: delegate to package CLI.

This file is a lightweight stub kept for compatibility; it forwards
invocations to `codex_task_runner.cli.cli`.
"""
from __future__ import annotations

import sys

from codex_task_runner.cli.cli import main


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))


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
    """Open Codex Cloud, click around, and log all API requests."""
    endpoints = []
    
    cookies = load_cookies_from_env()
    if not cookies:
        print("Warning: No cookies found in .env")
    else:
        print(f"Loaded {len(cookies)} cookies from .env")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars",
                "--no-first-run",
                "--no-default-browser-check",
            ]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            locale="en-US",
            timezone_id="America/New_York",
        )
        
        if cookies:
            await context.add_cookies(cookies)
        
        page = await context.new_page()
        
        # Apply playwright-stealth to avoid bot detection
        stealth = Stealth(navigator_platform_override="MacIntel")
        await stealth.apply_stealth_async(page)
        
        def log_request(request):
            url = request.url
            if "backend-api" in url or "wham" in url:
                entry = {
                    "method": request.method,
                    "url": url,
                }
                if request.method == "POST":
                    try:
                        entry["body"] = request.post_data
                    except:
                        pass
                endpoints.append(entry)
                print(f"{request.method} {url}")
        
        page.on("request", log_request)
        
        print("Opening Codex Cloud...")
        
        try:
            await page.goto("https://chatgpt.com/codex/", wait_until="domcontentloaded", timeout=60000)
        except Exception as e:
            print(f"Navigation: {e}")
        
        # Wait for page to load
        print("Waiting for tasks to load...")
        await asyncio.sleep(5)
        
        # Try to click on first task
        print("Looking for a task to click...")
        try:
            # Look for task links - they have /codex/tasks/ in href
            task_link = await page.locator('a[href*="/codex/tasks/task_"]').first.element_handle(timeout=10000)
            if task_link:
                print("Found a task, clicking...")
                await task_link.click()
                await asyncio.sleep(3)
                
                # Look for tabs/sections to click
                print("Looking for detail sections...")
                
                # Try clicking various UI elements that might trigger API calls
                for selector in [
                    'button:has-text("PR")',
                    'button:has-text("Code")', 
                    'button:has-text("Files")',
                    'button:has-text("Diff")',
                    '[data-testid*="pr"]',
                    '[data-testid*="code"]',
                ]:
                    try:
                        el = await page.locator(selector).first.element_handle(timeout=2000)
                        if el:
                            print(f"  Clicking: {selector}")
                            await el.click()
                            await asyncio.sleep(2)
                    except:
                        pass
        except Exception as e:
            print(f"Could not click task: {e}")
        
        # Keep running for manual exploration
        print("\nNow explore manually. Press Ctrl+C when done.\n")
        
        try:
            while True:
                await asyncio.sleep(1)
                if not browser.is_connected():
                    break
        except (KeyboardInterrupt, Exception):
            pass
        
        try:
            await browser.close()
        except:
            pass
    
    # Save discovered endpoints (always, even on interrupt)
    save_endpoints(endpoints, output_file)


def save_endpoints(endpoints, output_file):
    """Save endpoints to file and print summary."""
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
