"""Discover Codex API endpoints by intercepting browser traffic."""
import asyncio
import json
from pathlib import Path
from typing import Any

from playwright.async_api import async_playwright
from playwright_stealth import Stealth


async def _discover_endpoints(
    cookies: list[dict],
    output_file: str,
    timeout: int = 30,
    headless: bool = False,
) -> list[dict]:
    """Open Codex Cloud, click around, and log all API requests."""
    endpoints = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=headless,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars",
                "--no-first-run",
                "--no-default-browser-check",
            ],
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
                    except Exception:
                        pass
                endpoints.append(entry)
                print(f"{request.method} {url}")

        page.on("request", log_request)

        print("Opening Codex Cloud...")

        try:
            await page.goto(
                "https://chatgpt.com/codex/", wait_until="domcontentloaded", timeout=60000
            )
        except Exception as e:
            print(f"Navigation: {e}")

        # Wait for page to load
        print("Waiting for tasks to load...")
        await asyncio.sleep(5)

        # Try to click on first task
        print("Looking for a task to click...")
        try:
            task_link = await page.locator(
                'a[href*="/codex/tasks/task_"]'
            ).first.element_handle(timeout=10000)
            if task_link:
                print("Found a task, clicking...")
                await task_link.click()
                await asyncio.sleep(3)

                # Try clicking various UI elements that might trigger API calls
                print("Looking for detail sections...")
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
                    except Exception:
                        pass
        except Exception as e:
            print(f"Could not click task: {e}")

        if timeout > 0:
            print(f"\nWaiting {timeout}s for manual exploration (Ctrl+C to stop early)...")
            try:
                for _ in range(timeout):
                    await asyncio.sleep(1)
                    if not browser.is_connected():
                        break
            except (KeyboardInterrupt, Exception):
                pass
        else:
            print("\nNow explore manually. Close browser when done.\n")
            try:
                while browser.is_connected():
                    await asyncio.sleep(1)
            except (KeyboardInterrupt, Exception):
                pass

        try:
            await browser.close()
        except Exception:
            pass

    # Save discovered endpoints
    if endpoints and output_file:
        output = Path(output_file)
        output.write_text(json.dumps(endpoints, indent=2))
        print(f"\nSaved {len(endpoints)} endpoints to {output_file}")

    return endpoints


def _parse_cookies_from_session(session) -> list[dict]:
    """Parse cookies from session cookie string."""
    cookie_str = session.headers.get("Cookie", "")
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


def handle(args: Any, session) -> dict:
    """Discover API endpoints by intercepting browser traffic."""
    cookies = _parse_cookies_from_session(session)
    if not cookies:
        print("Warning: No cookies found in session")
    else:
        print(f"Loaded {len(cookies)} cookies from session")

    output_file = getattr(args, "output", "discovered_endpoints.json")
    timeout = getattr(args, "timeout", 30)
    headless = getattr(args, "headless", False)

    endpoints = asyncio.run(
        _discover_endpoints(cookies, output_file, timeout, headless)
    )

    # Extract unique endpoints
    unique = set()
    for e in endpoints:
        url = e["url"]
        if "backend-api" in url:
            path = url.split("backend-api")[1].split("?")[0]
            unique.add(f"{e['method']} /backend-api{path}")

    return {
        "total_requests": len(endpoints),
        "unique_endpoints": sorted(unique),
        "output_file": output_file,
    }
