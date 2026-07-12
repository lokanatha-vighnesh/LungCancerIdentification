import asyncio
import os
import urllib.parse as up
from playwright.async_api import async_playwright

URLS = [
    "https://cancer.sanger.ac.uk/cosmic/gene/analysis?all_data=n&hn=carcinoma&in=t&ln=EGFR&sh=&sn=lung&src=tissue&ss=all&wgs=off",
"https://cancer.sanger.ac.uk/cosmic/gene/analysis?all_data=n&hn=carcinoma&in=t&ln=KRAS&sh=&sn=lung&src=tissue&ss=all&wgs=off",
"https://cancer.sanger.ac.uk/cosmic/gene/analysis?all_data=n&hn=carcinoma&in=t&ln=TP53&sh=&sn=lung&src=tissue&ss=all&wgs=off",
"https://cancer.sanger.ac.uk/cosmic/gene/analysis?all_data=n&hn=carcinoma&in=t&ln=LRP1B&sh=&sn=lung&src=tissue&ss=all&wgs=off",
"https://cancer.sanger.ac.uk/cosmic/gene/analysis?all_data=n&hn=carcinoma&in=t&ln=PIK3CA&sh=&sn=lung&src=tissue&ss=all&wgs=off",
"https://cancer.sanger.ac.uk/cosmic/gene/analysis?all_data=n&hn=carcinoma&in=t&ln=STK11&sh=&sn=lung&src=tissue&ss=all&wgs=off",
"https://cancer.sanger.ac.uk/cosmic/gene/analysis?all_data=n&hn=carcinoma&in=t&ln=KEAP1&sh=&sn=lung&src=tissue&ss=all&wgs=off",
"https://cancer.sanger.ac.uk/cosmic/gene/analysis?all_data=n&hn=carcinoma&in=t&ln=BRAF&sh=&sn=lung&src=tissue&ss=all&wgs=off",
"https://cancer.sanger.ac.uk/cosmic/gene/analysis?all_data=n&hn=carcinoma&in=t&ln=RB1&sh=&sn=lung&src=tissue&ss=all&wgs=off",
"https://cancer.sanger.ac.uk/cosmic/gene/analysis?all_data=n&hn=carcinoma&in=t&ln=MET&sh=&sn=lung&src=tissue&ss=all&wgs=off",
"https://cancer.sanger.ac.uk/cosmic/gene/analysis?all_data=n&hn=carcinoma&in=t&ln=KMT2D&sh=&sn=lung&src=tissue&ss=all&wgs=off",
"https://cancer.sanger.ac.uk/cosmic/gene/analysis?all_data=n&hn=carcinoma&in=t&ln=ARID1A&sh=&sn=lung&src=tissue&ss=all&wgs=off",
"https://cancer.sanger.ac.uk/cosmic/gene/analysis?all_data=n&hn=carcinoma&in=t&ln=KMT2C&sh=&sn=lung&src=tissue&ss=all&wgs=off",
"https://cancer.sanger.ac.uk/cosmic/gene/analysis?all_data=n&hn=carcinoma&in=t&ln=NF1&sh=&sn=lung&src=tissue&ss=all&wgs=off",
"https://cancer.sanger.ac.uk/cosmic/gene/analysis?all_data=n&hn=carcinoma&in=t&ln=ERBB2&sh=&sn=lung&src=tissue&ss=all&wgs=off",
"https://cancer.sanger.ac.uk/cosmic/gene/analysis?all_data=n&hn=carcinoma&in=t&ln=FAT1&sh=&sn=lung&src=tissue&ss=all&wgs=off",
"https://cancer.sanger.ac.uk/cosmic/gene/analysis?all_data=n&hn=carcinoma&in=t&ln=ALK&sh=&sn=lung&src=tissue&ss=all&wgs=off",
"https://cancer.sanger.ac.uk/cosmic/gene/analysis?all_data=n&hn=carcinoma&in=t&ln=ATM&sh=&sn=lung&src=tissue&ss=all&wgs=off",
"https://cancer.sanger.ac.uk/cosmic/gene/analysis?all_data=n&hn=carcinoma&in=t&ln=SMARCA4&sh=&sn=lung&src=tissue&ss=all&wgs=off",
"https://cancer.sanger.ac.uk/cosmic/gene/analysis?all_data=n&hn=carcinoma&in=t&ln=CDKN2A&sh=&sn=lung&src=tissue&ss=all&wgs=off"
]

DOWNLOAD_DIR = "cosmic_mutations"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


# -------- Label extractor --------
def parse_cosmic_url(url):
    q = up.parse_qs(up.urlparse(url).query)
    gene = q.get("ln", ["unknown"])[0]
    tissue = q.get("sn", ["unknown"])[0]
    hist = q.get("hn", ["unknown"])[0]
    return f"{gene}_{tissue}_{hist}.csv"


# -------- Core logic --------
async def download_csv(page, url):
    print(f"\nProcessing: {url}")
    await page.goto(url, timeout=60000)

    # wait for full load
    await page.wait_for_load_state("networkidle")

    # ---- Ensure Variants section is visible ----
    try:
        await page.locator("text=Variants").scroll_into_view_if_needed()
        await page.click("text=Variants")
    except:
        pass  # already visible in new UI

    # ---- Wait for table ----
    await page.wait_for_selector("table", timeout=15000)

    # ---- Find CSV button ----
    # Try multiple selectors (COSMIC UI changes often)
    selectors = [
        "text=CSV",
        "text=Download CSV",
        "button:has-text('CSV')"
    ]

    download_button = None
    for sel in selectors:
        if await page.locator(sel).count() > 0:
            download_button = sel
            break

    if not download_button:
        print("CSV button not found")
        return

    # ---- Download ----
    async with page.expect_download() as download_info:
        await page.click(download_button)

    download = await download_info.value

    filename = parse_cosmic_url(url)
    save_path = os.path.join(DOWNLOAD_DIR, filename)

    await download.save_as(save_path)

    print(f"Saved: {save_path}")


# -------- Main --------
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # login required
        context = await browser.new_context(accept_downloads=True)
        page = await context.new_page()

        print("👉 Login manually once, then press ENTER here...")
        input()

        for url in URLS:
            await download_csv(page, url)
            await asyncio.sleep(2)  # avoid rate limits

        await browser.close()


asyncio.run(main())