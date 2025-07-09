import asyncio
from pyppeteer import launch

async def open_edge_and_navigate(url: str):
    browser = await launch(
        executablePath='C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
        headless=False,
        args=['--remote-debugging-port=9222']
    )
    page = await browser.newPage()
    await page.goto(url)
    print(f"🌀 Navigated to: {url}")
    await asyncio.sleep(10)  # Keep it open briefly
    await browser.close()
