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

load_dotenv(Path(__file__).parent.parent / ".env")

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
    captured_requests = []
    captured_ws = []
    
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
        
        # Capture ALL requests (especially POST)
        def on_request(req):
            if req.method == "POST" or "wham" in req.url or "backend-api" in req.url:
                body = None
                try:
                    body = req.post_data if req.post_data else None
                except:
                    body = "<binary>"
                entry = {
                    "method": req.method,
                    "url": req.url,
                    "headers": dict(req.headers),
                    "body": body
                }
                captured_requests.append(entry)
                print(f"\n>>> {req.method} {req.url}")
                if body:
                    print(f"    Body: {body[:500]}...")
                
                # Special handling for wham/tasks POST - save it immediately
                if req.method == "POST" and "/wham/tasks" in req.url and body:
                    print("\n" + "="*60)
                    print("*** CAPTURED TASK CREATION REQUEST ***")
                    print("="*60)
                    print(f"URL: {req.url}")
                    print(f"Headers: {dict(req.headers)}")
                    print(f"Body: {body}")
                    print("="*60)
                    # Save immediately
                    task_file = Path(__file__).parent / "wham_tasks_post.json"
                    task_file.write_text(json.dumps({
                        "url": req.url,
                        "headers": dict(req.headers),
                        "body": body
                    }, indent=2))
                    print(f"Saved to: {task_file}")
                    print("="*60 + "\n")
        
        # Capture WebSocket frames in detail
        def on_websocket(ws):
            print(f"\n>>> WebSocket OPENED: {ws.url}")
            captured_ws.append({"event": "open", "url": ws.url})
            
            def on_sent(data):
                print(f"    WS SENT: {data[:500] if isinstance(data, str) else data}")
                captured_ws.append({"event": "sent", "data": data if isinstance(data, str) else str(data)})
            
            def on_received(data):
                print(f"    WS RECV: {data[:500] if isinstance(data, str) else data}")
                captured_ws.append({"event": "received", "data": data if isinstance(data, str) else str(data)})
            
            def on_close():
                print(f"    WS CLOSED")
                captured_ws.append({"event": "close"})
            
            ws.on("framesent", on_sent)
            ws.on("framereceived", on_received)
            ws.on("close", on_close)
        
        page.on("request", on_request)
        page.on("websocket", on_websocket)
        
        print("="*60)
        print("INSTRUCTIONS:")
        print("1. Browser will open to Codex")
        print("2. Click 'New task' button")
        print("3. Select a repository/environment")
        print("4. Type a simple prompt like 'add a comment to README'")
        print("5. Submit the task")
        print("6. Wait a few seconds for the task to appear")
        print("7. Close the browser")
        print("="*60)
        print()
        
        print("Going to Codex...")
        try:
            await page.goto("https://chatgpt.com/codex/", wait_until="domcontentloaded", timeout=60000)
        except Exception as e:
            print(f"Navigation warning: {e}")
        
        await asyncio.sleep(5)
        
        # Dump HTML for analysis
        html = await page.content()
        html_file = Path(__file__).parent / "codex_page.html"
        html_file.write_text(html)
        print(f"\nDumped HTML to: {html_file}")
        print(f"HTML length: {len(html)} chars")
        
        # Also get a list of all buttons and inputs
        print("\n--- All buttons ---")
        buttons = await page.locator("button").all()
        for i, btn in enumerate(buttons[:20]):  # First 20
            try:
                text = await btn.text_content()
                aria = await btn.get_attribute("aria-label")
                testid = await btn.get_attribute("data-testid")
                print(f"  [{i}] text='{text[:50] if text else ''}' aria='{aria}' testid='{testid}'")
            except:
                pass
        
        print("\n--- All textareas ---")
        textareas = await page.locator("textarea").all()
        for i, ta in enumerate(textareas):
            try:
                placeholder = await ta.get_attribute("placeholder")
                name = await ta.get_attribute("name")
                testid = await ta.get_attribute("data-testid")
                print(f"  [{i}] placeholder='{placeholder}' name='{name}' testid='{testid}'")
            except:
                pass
        
        print("\n--- All contenteditable ---")
        editables = await page.locator("[contenteditable='true']").all()
        for i, el in enumerate(editables):
            try:
                tag = await el.evaluate("el => el.tagName")
                cls = await el.get_attribute("class")
                print(f"  [{i}] tag={tag} class='{cls[:80] if cls else ''}'")
            except:
                pass
        
        print("\n--- All inputs ---")
        inputs = await page.locator("input").all()
        for i, inp in enumerate(inputs[:10]):
            try:
                typ = await inp.get_attribute("type")
                placeholder = await inp.get_attribute("placeholder")
                name = await inp.get_attribute("name")
                print(f"  [{i}] type='{typ}' placeholder='{placeholder}' name='{name}'")
            except:
                pass
        
        print("\nLooking for New Task button...")
        
        # The page already has the input visible - no need to click "New Task"
        # Just find the input directly
        
        # Look for the prompt input - try ProseMirror first (the actual visible editor)
        print("\nLooking for prompt input...")
        
        input_found = None
        
        # ProseMirror is the actual visible editor
        try:
            pm = page.locator('.ProseMirror')
            if await pm.count() > 0:
                input_found = pm.first
                print("  Found: .ProseMirror (contenteditable)")
        except:
            pass
        
        if not input_found:
            try:
                ta = page.locator('textarea[name="prompt-textarea"]')
                if await ta.count() > 0:
                    input_found = ta
                    print("  Found: textarea[name='prompt-textarea']")
            except:
                pass
        
        if input_found:
            try:
                await input_found.click(timeout=5000)
            except Exception as e:
                print(f"  Click failed: {e}")
            await asyncio.sleep(0.5)
            
            test_prompt = "ignore this test prompt - API capture test"
            print(f"\nTyping: '{test_prompt}'")
            
            # For ProseMirror, use keyboard.type instead of fill
            try:
                await input_found.fill(test_prompt)
            except:
                await page.keyboard.type(test_prompt, delay=50)
            
            await asyncio.sleep(1)
            
            # Find submit button - based on HTML: aria='Submit'
            print("\nLooking for submit button...")
            try:
                submit_btn = page.locator('button[aria-label="Submit"]')
                if await submit_btn.count() > 0:
                    print("  Found: button[aria-label='Submit']")
                    print("  Clicking submit...")
                    await submit_btn.click()
                    print("  Submitted! Waiting for WebSocket messages...")
                    await asyncio.sleep(15)  # Wait for task creation WS messages
            except Exception as e:
                print(f"  Submit error: {e}")
                # Try Enter key as fallback
                print("  Trying Ctrl+Enter...")
                await page.keyboard.press("Control+Enter")
                await asyncio.sleep(15)
        else:
            print("  No input found!")
        
        print("\n" + "="*60)
        print("Waiting 10 seconds to capture any follow-up requests...")
        print("Close browser manually if needed.")
        print("="*60)
        
        await asyncio.sleep(10)
        
        # Wait for browser to close or timeout
        try:
            for _ in range(30):  # Wait up to 30 more seconds
                if not browser.is_connected():
                    break
                await asyncio.sleep(1)
        except:
            pass
        
        try:
            await browser.close()
        except:
            pass
    
    # Save captured data
    output = {
        "requests": captured_requests,
        "websocket_frames": captured_ws
    }
    
    output_file = Path(__file__).parent / "task_creation_capture.json"
    output_file.write_text(json.dumps(output, indent=2))
    
    print("\n" + "="*60)
    print(f"CAPTURED: {len(captured_requests)} HTTP requests, {len(captured_ws)} WebSocket frames")
    print(f"Saved to: {output_file}")
    print("="*60)
    
    # Print summary of interesting endpoints
    print("\nPOST requests to backend-api:")
    for req in captured_requests:
        if req["method"] == "POST" and "backend-api" in req["url"]:
            print(f"  {req['url']}")
            if req.get("body"):
                try:
                    body = json.loads(req["body"])
                    print(f"    {json.dumps(body, indent=4)[:300]}")
                except:
                    print(f"    {req['body'][:200]}")
    
    print("\nWebSocket messages with 'task' or 'wham':")
    for ws in captured_ws:
        if ws.get("data"):
            data = ws["data"]
            if "task" in data.lower() or "wham" in data.lower() or "prompt" in data.lower():
                print(f"  [{ws['event']}] {data[:300]}")


if __name__ == "__main__":
    asyncio.run(main())
