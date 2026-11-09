#!/usr/bin/env python3
"""Configurable Playwright probe for a site where automated access is authorized.

This intentionally does not bypass CAPTCHAs, logins, bot checks, queues or paywalls.
Configure a search URL template and CSS selector only after checking the site's terms
and obtaining permission where required.
"""
import datetime as dt
import json
import os
import pathlib
import re
from playwright.sync_api import sync_playwright

def main():
    template = os.environ.get("BROWSER_SEARCH_URL_TEMPLATE", "").strip()
    selector = os.environ.get("BROWSER_PRICE_SELECTOR", "").strip()
    if not template or not selector:
        print("Browser probe skipped: configure BROWSER_SEARCH_URL_TEMPLATE and BROWSER_PRICE_SELECTOR.")
        return

    origin = os.environ.get("ORIGIN", "BCN").strip().upper()
    destination = os.environ.get("DESTINATION", "FEZ").strip().upper()
    departure_date = dt.date.fromisoformat(os.environ["DEPARTURE_DATE"])
    url = template.format(origin=origin, destination=destination, date=departure_date.isoformat())

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(locale="es-ES")
        page.set_default_timeout(25000)
        response = page.goto(url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(2500)
        title = page.title()
        # Stop rather than attempting to defeat access controls.
        body = (page.locator("body").inner_text(timeout=10000) or "")[:5000]
        lowered = body.lower()
        if any(marker in lowered for marker in ("captcha", "verify you are human", "access denied", "robot check")):
            browser.close()
            raise SystemExit("Access challenge/block detected. Probe stopped; no bypass attempted.")
        texts = page.locator(selector).all_inner_texts()
        browser.close()

    prices = []
    for text in texts:
        clean = " ".join(text.split())
        match = re.search(r"(\d[\d.,\s]*\d|\d)\s*(€|EUR|£|GBP|\$|USD)", clean, re.I)
        prices.append({"raw_text": clean[:250], "matched_price_text": match.group(0) if match else None})

    result = {
        "source": "authorized browser probe",
        "updated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "origin": origin, "destination": destination,
        "departure_date": departure_date.isoformat(),
        "page_title": title,
        "http_status": response.status if response else None,
        "result_count": len(texts),
        "results": prices,
        "status": "unverified",
        "note": "DOM extraction only. Confirm site terms/permission; no CAPTCHA or access-control bypass.",
    }
    out = pathlib.Path("data/browser-probe-results.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Browser probe saved {len(texts)} matching elements from {url}")

if __name__ == "__main__":
    main()
