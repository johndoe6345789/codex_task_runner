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

def get_cookies():
    cookie_str = os.getenv("COOKIE", "")
    cookies = []
    for part in cookie_str.split(";"):
        part = part.strip()
        if "=" in part:
            name, value = part.split("=", 1)
            cookies.append({
                "name": name.strip(),
                "value": value.strip(),
                "domain": "chatgpt.com",
                "path": "/",
                "secure": True,
                "httpOnly": False,
                "sameSite": "Lax",
            })
    return cookies


async def main():
    captured = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            viewport={"width": 1920, "height": 1080}
        )
        await context.add_cookies(get_cookies())
        
        page = await context.new_page()
        stealth = Stealth(navigator_platform_override="MacIntel")
        await stealth.apply_stealth_async(page)
        
        # Capture ALL requests
        def on_request(req):
            if req.method == "POST":
                body = None
                try:
                    body = req.post_data[:2000] if req.post_data else None
                except:
                    body = "<binary>"
                entry = {
                    "method": req.method,
                    "url": req.url,
                    "body": body
                }
                captured.append(entry)
                print(f"\n>>> POST {req.url}")
                if body and body != "<binary>":
                    print(f"    Body: {body[:500]}...")
        
        # Capture WebSocket messages
        def on_websocket(ws):
            print(f"\n>>> WebSocket: {ws.url}")
            ws.on("framesent", lambda data: print(f"    WS SENT: {str(data)[:200]}"))
            ws.on("framereceived", lambda data: print(f"    WS RECV: {str(data)[:200]}"))
        
        page.on("request", on_request)
        page.on("websocket", on_websocket)
        
        print("Going to Codex...")
        await page.goto("https://chatgpt.com/codex/", wait_until="networkidle", timeout=60000)
        await asyncio.sleep(3)
        
        print("\nLooking for New Task button...")
        
        # Click New Task button
        new_btn = page.locator('button[aria-label*="New"], button[aria-label*="new"]').first
        if await new_btn.count() > 0:
            print("Clicking New Task button...")
            await new_btn.click()
            await asyncio.sleep(2)
        
        # Find the textarea/input for prompt
        print("Looking for prompt input...")
        selectors = [
            'textarea',
            'div[contenteditable="true"]',
            'input[type="text"]',
            '[data-testid*="input"]',
            '[data-testid*="prompt"]',
            '.ProseMirror',
        ]
        
        for sel in selectors:
            el = page.locator(sel).first
            if await el.count() > 0:
                print(f"Found input: {sel}")
                await el.click()
                await asyncio.sleep(0.5)
                
                # Type test prompt
                test_prompt = "test prompt - please ignore and delete this task"
                print(f"Typing: {test_prompt}")
                await el.fill(test_prompt)
                await asyncio.sleep(1)
                break
        
        print("\n" + "="*60)
        print("MANUAL STEP: Please submit the task (press Enter or click Send)")
        print("Watch for POST requests in the output above")
        print("Close browser when done")
        print("="*60 + "\n")
        
        # Wait for browser close
        try:
            while browser.is_connected():
                await asyncio.sleep(1)
        except:
            pass
        
        await browser.close()
    
    # Print summary
    print("\n" + "="*60)
    print("CAPTURED POST REQUESTS:")
    print("="*60)
    for req in captured:
        print(f"\n{req['method']} {req['url']}")
        if req.get('body'):
            try:
                body = json.loads(req['body'])
                print(json.dumps(body, indent=2)[:1000])
            except:
                print(req['body'][:500])
    
    # Save to file
    Path("create_task_endpoints.json").write_text(json.dumps(captured, indent=2))
    print(f"\nSaved {len(captured)} requests to create_task_endpoints.json")


if __name__ == "__main__":
    asyncio.run(main())
