"""Discover Codex API endpoints by intercepting browser traffic."""
import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright


async def discover_endpoints(output_file: str = "discovered_endpoints.json"):
    """Open Codex Cloud and log all API requests."""
    endpoints = []
    
    async with async_playwright() as p:
        # Launch browser (not headless so user can interact)
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        # Intercept all requests
        async def log_request(request):
            url = request.url
            if "codex" in url.lower() or "backend-api" in url or "wham" in url:
                entry = {
                    "method": request.method,
                    "url": url,
                    "headers": dict(request.headers),
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
        print("Opening Codex Cloud - interact with the UI to discover endpoints")
        print("Press Ctrl+C when done\n")
        
        await page.goto("https://codex.openai.com/")
        
        # Keep running until user stops
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            pass
        
        await browser.close()
    
    # Save discovered endpoints
    output = Path(output_file)
    output.write_text(json.dumps(endpoints, indent=2))
    print(f"\nSaved {len(endpoints)} endpoints to {output_file}")
    
    # Print unique endpoints
    unique = set()
    for e in endpoints:
        # Extract path from URL
        url = e["url"]
        if "backend-api" in url:
            path = url.split("backend-api")[1].split("?")[0]
            unique.add(f"{e['method']} /backend-api{path}")
    
    print("\nUnique endpoints:")
    for ep in sorted(unique):
        print(f"  {ep}")


if __name__ == "__main__":
    asyncio.run(discover_endpoints())
